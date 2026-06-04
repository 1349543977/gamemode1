# 虚拟现实人生养成游戏 - MVP 设计文档

> 日期: 2026-06-04
> 版本: 1.0
> 状态: 待审核

## 1. 项目概述

### 1.1 产品定位

一款跨微信小程序、安卓、苹果端的虚拟现实人生养成游戏。玩家作为"观察者"与"引导者"，看着角色在虚拟地球上生活，通过干预角色的关键决策影响其人生走向。

### 1.2 MVP范围

MVP聚焦核心玩法循环：**角色创建 → 时间推进 → 事件触发 → 玩家干预 → 属性变化 → 人生记录**。社交系统、AI生成事件、世界演变等高级功能留待后续迭代。

### 1.3 核心决策记录

| 决策项 | 选择 | 理由 |
|--------|------|------|
| 项目范围 | MVP优先 | 降低风险，快速验证核心玩法 |
| 地球渲染 | 2D手绘地图 | 性能好、包体小、小程序兼容性强 |
| AI集成 | 规则引擎优先 | 稳定可控、无外部依赖、零额外成本 |
| 后端部署 | 独立服务器 | 架构简单可控、不绑定微信生态 |
| 前端框架 | Taro + React | 小程序兼容性最佳、React+TS生态成熟 |
| 时间推进 | 手动推进 | 玩家可控、适合碎片化玩法 |
| 时间比例 | 现实1小时 = 游戏1年 | 充裕决策时间、适合移动端 |

## 2. 系统架构

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────┐
│                    客户端层                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │微信小程序 │  │  H5/Web  │  │React Native│         │
│  └────┬─────┘  └────┬─────┘  └────┬──────┘         │
│       └──────────┬───┘────────────┘                 │
│            Taro 统一前端                              │
│  ┌──────────────────────────────────────────────┐   │
│  │ Presentation (Pages/Components)              │   │
│  │ Domain (Hooks/Store/Types)                   │   │
│  │ Data (API Client/Cache/WS)                   │   │
│  └──────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────┘
                       │ HTTPS / WSS
┌──────────────────────┴──────────────────────────────┐
│                    API 网关层                         │
│              Nginx + SSL + Rate Limit                │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────┐
│                  应用服务层 (FastAPI)                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │ Auth服务  │ │ Game服务  │ │ Event服务 │           │
│  └──────────┘ └──────────┘ └──────────┘            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │角色服务   │ │时间服务   │ │规则引擎   │           │
│  └──────────┘ └──────────┘ └──────────┘            │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────┐
│                   数据层                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │  MySQL   │  │  Redis   │  │ Celery   │          │
│  │ 持久存储  │  │ 缓存/会话 │  │ 异步任务  │         │
│  └──────────┘  └──────────┘  └──────────┘          │
└─────────────────────────────────────────────────────┘
```

### 2.2 架构原则

- **Clean Architecture**: 依赖方向从外向内，领域层不依赖任何框架
- **Repository Pattern**: 服务层通过Repository接口访问数据，禁止直接操作ORM
- **依赖注入**: FastAPI原生DI，所有服务可替换可测试
- **事件驱动**: 角色状态变更发出领域事件，解耦业务逻辑
- **配置外置**: 所有环境变量通过 `.env` 管理，零硬编码

### 2.3 技术栈

**前端:**
- Taro 4.x - 跨端框架
- React 18 - UI库
- TypeScript 5 - 类型安全
- Zustand - 客户端状态管理
- TanStack Query - 服务端状态管理
- NutUI (Taro版) - 京东出品UI组件库，原生支持Taro跨端

**后端:**
- FastAPI - Web框架
- SQLAlchemy 2.0 - ORM
- Alembic - 数据库迁移
- Redis - 缓存/会话
- Celery - 异步任务队列
- MySQL 8.0 - 持久存储
- Pydantic v2 - 数据校验

**基础设施:**
- Docker + Docker Compose - 容器化
- Nginx - 反向代理/SSL/限流
- GitHub Actions - CI/CD

## 3. 数据库设计

### 3.1 ER关系概览

```
users 1──N characters 1──1 character_stats
                  │
                  ├──N life_records
                  ├──N relationships
                  ├──N assets
                  └──N (event_results via events)

events 1──N event_results

cities 1──N characters
jobs (独立参考表)
world_states (独立时间序列表)
```

### 3.2 表结构详细设计

#### users - 用户表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 用户ID |
| openid | VARCHAR(128) | UNIQUE, NOT NULL | 微信openid |
| union_id | VARCHAR(128) | UNIQUE, NULLABLE | 微信unionid（跨端关联） |
| phone | VARCHAR(20) | UNIQUE, NULLABLE | 绑定手机号 |
| nickname | VARCHAR(50) | NOT NULL | 昵称 |
| avatar_url | VARCHAR(500) | NULLABLE | 头像URL |
| platform | VARCHAR(20) | NOT NULL | 注册平台: wechat/ios/android |
| last_login_at | DATETIME | NOT NULL | 最后登录时间 |
| created_at | DATETIME | NOT NULL, DEFAULT NOW | 创建时间 |
| updated_at | DATETIME | NOT NULL, DEFAULT NOW | 更新时间 |

#### characters - 角色表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 角色ID |
| user_id | BIGINT | FK → users.id, NOT NULL | 所属用户 |
| name | VARCHAR(50) | NOT NULL | 角色姓名 |
| gender | ENUM('male','female') | NOT NULL | 性别 |
| birth_year | INT | NOT NULL | 出生年份（游戏内） |
| age | INT | NOT NULL, DEFAULT 0 | 当前年龄 |
| stage | VARCHAR(20) | NOT NULL | 人生阶段 |
| is_alive | BOOLEAN | NOT NULL, DEFAULT TRUE | 是否存活 |
| city_id | BIGINT | FK → cities.id, NOT NULL | 所在城市 |
| lifespan | INT | NOT NULL, DEFAULT 75 | 预期寿命 |
| death_cause | VARCHAR(100) | NULLABLE | 死因 |
| created_at | DATETIME | NOT NULL | 创建时间 |
| updated_at | DATETIME | NOT NULL | 更新时间 |

#### character_stats - 角色属性表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 属性ID |
| character_id | BIGINT | FK → characters.id, UNIQUE, NOT NULL | 角色ID |
| health | INT | NOT NULL, DEFAULT 60 | 健康 (0-100) |
| intelligence | INT | NOT NULL, DEFAULT 50 | 智力 (0-100) |
| charisma | INT | NOT NULL, DEFAULT 50 | 魅力 (0-100) |
| wealth | INT | NOT NULL, DEFAULT 30 | 财富 (0-100) |
| happiness | INT | NOT NULL, DEFAULT 60 | 幸福 (0-100) |
| luck | INT | NOT NULL, DEFAULT 50 | 运气 (0-100) |
| updated_at | DATETIME | NOT NULL | 更新时间 |

#### life_records - 人生记录表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 记录ID |
| character_id | BIGINT | FK → characters.id, NOT NULL | 角色ID |
| age | INT | NOT NULL | 记录时年龄 |
| year | INT | NOT NULL | 游戏内年份 |
| summary | TEXT | NOT NULL | 年度总结文本 |
| stat_changes | JSON | NULLABLE | 属性变化记录 |
| created_at | DATETIME | NOT NULL | 创建时间 |

#### events - 事件表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 事件ID |
| title | VARCHAR(100) | NOT NULL | 事件标题 |
| description | TEXT | NOT NULL | 事件描述 |
| stage | VARCHAR(20) | NOT NULL | 适用人生阶段 |
| category | VARCHAR(30) | NOT NULL | 事件分类 |
| trigger_condition | JSON | NOT NULL | 触发条件 |
| probability | FLOAT | NOT NULL, DEFAULT 1.0 | 触发概率 (0-1) |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | 是否启用 |
| created_at | DATETIME | NOT NULL | 创建时间 |

#### event_results - 事件结果表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 结果ID |
| event_id | BIGINT | FK → events.id, NOT NULL | 事件ID |
| choice_text | VARCHAR(200) | NOT NULL | 选项文本 |
| choice_index | INT | NOT NULL | 选项序号 |
| effects | JSON | NOT NULL | 效果: {"health": -10, "intelligence": 5} |
| narrative | TEXT | NOT NULL | 选择后的叙事文本 |
| next_event_id | BIGINT | FK → events.id, NULLABLE | 连锁事件 |
| created_at | DATETIME | NOT NULL | 创建时间 |

#### relationships - 关系表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 关系ID |
| character_id | BIGINT | FK → characters.id, NOT NULL | 角色ID |
| target_name | VARCHAR(50) | NOT NULL | 关系对象姓名 |
| type | VARCHAR(20) | NOT NULL | 关系类型: family/friend/lover/colleague |
| intimacy | INT | NOT NULL, DEFAULT 50 | 亲密度 (0-100) |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | 关系是否有效 |
| created_at | DATETIME | NOT NULL | 创建时间 |
| updated_at | DATETIME | NOT NULL | 更新时间 |

#### cities - 城市表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 城市ID |
| name | VARCHAR(50) | NOT NULL | 城市名称 |
| region | VARCHAR(50) | NOT NULL | 所属区域 |
| population | INT | NOT NULL | 人口规模 |
| development_index | FLOAT | NOT NULL | 发展指数 (0-1) |
| cost_of_living | FLOAT | NOT NULL | 生活成本指数 |
| created_at | DATETIME | NOT NULL | 创建时间 |

#### jobs - 职业表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 职业ID |
| name | VARCHAR(50) | NOT NULL | 职业名称 |
| category | VARCHAR(30) | NOT NULL | 职业分类 |
| min_intelligence | INT | NOT NULL, DEFAULT 0 | 最低智力要求 |
| min_charisma | INT | NOT NULL, DEFAULT 0 | 最低魅力要求 |
| salary_range | JSON | NOT NULL | 薪资范围: {"min": 3000, "max": 8000} |
| stress_level | INT | NOT NULL, DEFAULT 50 | 压力等级 (0-100) |
| health_impact | INT | NOT NULL, DEFAULT 0 | 健康影响 |
| created_at | DATETIME | NOT NULL | 创建时间 |

#### assets - 资产表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 资产ID |
| character_id | BIGINT | FK → characters.id, NOT NULL | 角色ID |
| type | VARCHAR(20) | NOT NULL | 资产类型: property/vehicle/savings/investment |
| name | VARCHAR(100) | NOT NULL | 资产名称 |
| value | DECIMAL(12,2) | NOT NULL | 资产价值 |
| acquired_age | INT | NOT NULL | 获得时年龄 |
| created_at | DATETIME | NOT NULL | 创建时间 |

#### world_states - 世界状态表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 状态ID |
| year | INT | NOT NULL, UNIQUE | 游戏内年份 |
| era | VARCHAR(30) | NOT NULL | 时代名称 |
| gdp_index | FLOAT | NOT NULL | GDP指数 |
| tech_level | INT | NOT NULL | 科技水平 (1-10) |
| major_events | JSON | NULLABLE | 重大事件列表 |
| updated_at | DATETIME | NOT NULL | 更新时间 |

### 3.3 索引设计

```sql
-- 高频查询索引
CREATE INDEX idx_characters_user_id ON characters(user_id);
CREATE INDEX idx_characters_stage ON characters(stage);
CREATE INDEX idx_life_records_character_age ON life_records(character_id, age);
CREATE INDEX idx_events_stage_category ON events(stage, category);
CREATE INDEX idx_event_results_event_id ON event_results(event_id);
CREATE INDEX idx_relationships_character_id ON relationships(character_id);
CREATE INDEX idx_world_states_year ON world_states(year);
```

## 4. API设计

### 4.1 通用规范

- 基础路径: `/api/v1/`
- 认证方式: Bearer Token (JWT)
- 内容类型: `application/json`
- 错误格式: `{"error": {"code": "ERROR_CODE", "message": "描述"}}`
- 分页: `?page=1&page_size=20`
- 所有接口提供Swagger文档

### 4.2 认证模块

#### POST /api/v1/auth/wechat-login
微信登录，传入code换取openid，返回JWT。

**请求:**
```json
{
  "code": "微信登录code",
  "platform": "wechat"
}
```

**响应:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 86400,
  "user": {
    "id": 1,
    "nickname": "玩家昵称",
    "avatar_url": "https://...",
    "has_phone": false
  }
}
```

#### POST /api/v1/auth/phone-bind
绑定手机号，实现跨端数据互通。

**请求:**
```json
{
  "phone": "13800138000",
  "verify_code": "123456"
}
```

#### POST /api/v1/auth/refresh
刷新Token。

#### GET /api/v1/auth/profile
获取当前用户信息。

### 4.3 角色模块

#### POST /api/v1/characters
创建新角色。

**请求:**
```json
{
  "name": "张三",
  "gender": "male",
  "city_id": 1
}
```

**响应:**
```json
{
  "id": 1,
  "name": "张三",
  "gender": "male",
  "age": 0,
  "stage": "infant",
  "is_alive": true,
  "city": {
    "id": 1,
    "name": "北京"
  },
  "stats": {
    "health": 65,
    "intelligence": 48,
    "charisma": 52,
    "wealth": 30,
    "happiness": 70,
    "luck": 45
  }
}
```

#### GET /api/v1/characters/{id}
获取角色详情（含属性和当前状态）。

#### GET /api/v1/characters/{id}/stats
获取角色属性（6维）。

#### GET /api/v1/characters/{id}/life-records?page=1&page_size=20
获取人生记录（分页）。

### 4.4 时间模块

#### POST /api/v1/characters/{id}/advance
推进时间1年。核心玩法接口。

**响应:**
```json
{
  "character": {
    "age": 7,
    "stage": "childhood"
  },
  "year_summary": {
    "stat_changes": {
      "health": 2,
      "intelligence": 5
    },
    "events_triggered": [1, 5],
    "new_relationships": []
  },
  "pending_events": [
    {
      "id": 1,
      "title": "入学考试",
      "description": "你到了上学的年纪，父母为你选择了一所小学...",
      "choices": [
        {
          "index": 0,
          "text": "努力学习，争取好成绩"
        },
        {
          "index": 1,
          "text": "交朋友更重要"
        }
      ]
    }
  ]
}
```

#### GET /api/v1/characters/{id}/timeline
获取角色完整时间线。

#### WebSocket /ws/v1/characters/{id}/live
实时推送角色状态变化和事件通知。

### 4.5 事件模块

#### GET /api/v1/characters/{id}/events/pending
获取角色当前待处理事件列表。

#### POST /api/v1/events/{id}/choose
玩家选择事件选项。

**请求:**
```json
{
  "character_id": 1,
  "choice_index": 0
}
```

**响应:**
```json
{
  "narrative": "你刻苦学习，成绩名列前茅，老师们对你赞不绝口。",
  "effects": {
    "intelligence": 8,
    "happiness": -2,
    "charisma": -3
  },
  "new_stats": {
    "health": 67,
    "intelligence": 61,
    "charisma": 47,
    "wealth": 30,
    "happiness": 68,
    "luck": 45
  },
  "triggered_events": [
    {
      "id": 15,
      "title": "被选为班长",
      "description": "因为你成绩优异，老师推荐你当班长..."
    }
  ]
}
```

#### GET /api/v1/events/{id}/result
获取事件结果详情。

### 4.6 世界模块

#### GET /api/v1/world/state
获取当前世界状态。

#### GET /api/v1/cities
获取城市列表。

#### GET /api/v1/jobs
获取职业列表（支持按属性筛选）。

## 5. 核心游戏系统

### 5.1 时间与成长系统

**时间比例:** 现实1小时 = 游戏1年（手动推进模式）

**推进流程:**
1. 玩家点击"度过这一年"按钮
2. 系统计算年龄+1
3. 判断人生阶段是否转换
4. 规则引擎判定本年触发的事件
5. 生成年度属性自然变化（基于年龄和当前属性）
6. 返回年度总结 + 待处理事件列表
7. 玩家处理完所有事件后，该年结束

**人生阶段划分:**

| 阶段 | 年龄 | 英文标识 | 核心事件类型 |
|------|------|----------|-------------|
| 婴儿期 | 0-3 | infant | 健康、家庭环境 |
| 幼儿期 | 4-6 | toddler | 性格形成、启蒙教育 |
| 少年期 | 7-12 | childhood | 学业、友谊、兴趣 |
| 青春期 | 13-18 | adolescence | 升学、初恋、叛逆 |
| 青年期 | 19-30 | youth | 大学、择业、恋爱、婚姻 |
| 壮年期 | 31-50 | prime | 事业、家庭、健康危机 |
| 中年期 | 51-65 | middle_age | 事业巅峰/危机、子女、养老规划 |
| 老年期 | 66+ | elderly | 退休、疾病、回忆、离世 |

### 5.2 属性系统

**6维属性 (0-100):**

| 属性 | 英文 | 影响 | 自然变化趋势 |
|------|------|------|-------------|
| 健康 | health | 寿命、疾病概率 | 青年巅峰后缓慢下降 |
| 智力 | intelligence | 升学、职业选择 | 青年期快速增长，老年缓降 |
| 魅力 | charisma | 社交、恋爱 | 青年期最高，中年后下降 |
| 财富 | wealth | 生活品质、医疗 | 壮年期积累，老年消耗 |
| 幸福 | happiness | 心理健康、决策倾向 | 受事件影响波动大 |
| 运气 | luck | 随机修正因子 | 随机波动 |

**属性自然变化规则:**
- 每年基础变化基于年龄和当前值计算
- 健康在30岁后每年-0.5~-1.5（基于当前值）
- 智力在25岁前每年+1~3，60岁后每年-0.5~1
- 财富受职业和年龄影响
- 运气每年随机-5~+5

### 5.3 事件与规则引擎系统

**事件触发流程:**
1. 时间推进时，规则引擎扫描所有适用事件
2. 基于条件（阶段、属性阈值、前置事件）筛选候选事件
3. 按概率判定是否触发
4. 每年最多触发1-3个事件（避免决策疲劳）
5. 优先级: 阶段必触发事件 > 连锁事件 > 随机事件

**事件分类（MVP首批约110种）:**

| 分类 | 数量 | 示例 |
|------|------|------|
| 升学事件 | ~20 | 小升初、中考、高考、考研 |
| 职业事件 | ~30 | 求职、升职、裁员、创业 |
| 健康事件 | ~20 | 疾病、意外、体检 |
| 社交事件 | ~25 | 交友、恋爱、婚姻、冲突 |
| 随机事件 | ~15 | 中奖、灾害、奇遇 |

**规则引擎核心逻辑:**
```python
class RuleEngine:
    def evaluate_events(self, character: Character, age: int) -> list[Event]:
        candidates = self.get_applicable_events(character.stage, age)
        triggered = []
        for event in candidates:
            if self.check_conditions(event.trigger_condition, character):
                if random() < event.probability:
                    triggered.append(event)
        return self.prioritize(triggered)[:3]  # 最多3个事件
```

### 5.4 角色生命周期状态机

```
[创建] → [infant] → [toddler] → [childhood] → [adolescence]
                                                │
[death] ← [elderly] ← [middle_age] ← [prime] ← [youth]
```

**死亡判定:**
- 健康 ≤ 0 → 立即死亡
- 年龄超过动态寿命阈值 → 概率死亡（健康越低概率越高）
- 特殊事件导致意外死亡

**寿命计算:**
```
base_lifespan = 75
health_modifier = (health - 50) * 0.3
wealth_modifier = (wealth - 50) * 0.1
effective_lifespan = base_lifespan + health_modifier + wealth_modifier
```

## 6. UI设计

### 6.1 页面结构

```
启动/登录页 → 首页/角色列表 → 角色创建页
                                    │
                              主游戏页（核心）
                              ├── 地图Tab: 2D手绘地图 + 角色位置
                              ├── 属性Tab: 6维雷达图 + 详细数值
                              ├── 记录Tab: 人生时间线
                              └── 设置Tab: 游戏设置
                                    │
                              年度总结页（推进后弹出）
                              ├── 今年发生的事
                              ├── 属性变化动画
                              └── 新建立的关系
```

### 6.2 设计原则

- **移动端优先**: 单手操作，按钮≥44px触摸区域
- **深色模式**: CSS变量统一管理，跟随系统或手动切换
- **Skeleton加载**: 所有页面有骨架屏过渡
- **表单校验**: 角色创建等表单实时校验
- **Loading状态**: 所有按钮点击后显示loading，防止重复提交
- **Design Token**: 统一颜色、间距、字体、圆角、阴影

### 6.3 Design Token 定义

```typescript
const tokens = {
  color: {
    primary: '#6366F1',      // 靛蓝
    secondary: '#8B5CF6',    // 紫色
    success: '#10B981',      // 绿色
    warning: '#F59E0B',      // 橙色
    danger: '#EF4444',       // 红色
    background: '#FFFFFF',   // 亮色背景
    surface: '#F8FAFC',      // 亮色表面
    text: '#1E293B',         // 主文字
    textSecondary: '#64748B', // 次要文字
  },
  darkColor: {
    background: '#0F172A',
    surface: '#1E293B',
    text: '#F1F5F9',
    textSecondary: '#94A3B8',
  },
  spacing: { xs: 4, sm: 8, md: 16, lg: 24, xl: 32 },
  fontSize: { xs: 12, sm: 14, md: 16, lg: 20, xl: 24, xxl: 32 },
  radius: { sm: 4, md: 8, lg: 12, xl: 16, full: 9999 },
};
```

### 6.4 小程序分包策略

```
主包 (< 4MB):
- 登录页、首页/角色列表
- 核心框架代码、状态管理、API层、类型定义

分包1 - game (< 2MB):
- 主游戏页、事件弹窗、年度总结

分包2 - assets (远程加载):
- 2D地图资源、角色立绘、音效
- 通过CDN按需加载
```

## 7. 项目结构

### 7.1 前端项目结构

```
client/
├── src/
│   ├── app.config.ts          # Taro应用配置（含分包）
│   ├── app.tsx                # 入口
│   ├── styles/
│   │   ├── tokens.ts          # Design tokens
│   │   ├── dark-mode.css      # 深色模式变量
│   │   └── global.css         # 全局样式
│   ├── components/            # 通用组件
│   │   ├── ui/                # NutUI组件封装层
│   │   │   ├── Button/
│   │   │   ├── Card/
│   │   │   ├── Dialog/
│   │   │   └── Skeleton/
│   │   ├── AttributeRadar/    # 属性雷达图
│   │   ├── EventCard/         # 事件卡片
│   │   ├── CharacterAvatar/   # 角色立绘
│   │   └── WorldMap/          # 2D手绘地图
│   ├── pages/                 # 页面
│   │   ├── index/             # 首页/角色列表
│   │   ├── login/             # 登录
│   │   ├── character-create/  # 角色创建
│   │   ├── game/              # 主游戏页
│   │   │   ├── index.tsx
│   │   │   ├── MapTab.tsx
│   │   │   ├── StatsTab.tsx
│   │   │   └── RecordsTab.tsx
│   │   ├── year-summary/      # 年度总结
│   │   └── settings/          # 设置
│   ├── stores/                # Zustand状态管理
│   │   ├── useAuthStore.ts
│   │   ├── useGameStore.ts
│   │   └── useCharacterStore.ts
│   ├── services/              # API调用层
│   │   ├── api.ts             # Axios实例
│   │   ├── auth.ts
│   │   ├── character.ts
│   │   ├── event.ts
│   │   └── world.ts
│   ├── hooks/                 # 自定义Hooks
│   │   ├── useWebSocket.ts
│   │   ├── useGameLoop.ts
│   │   └── useTheme.ts
│   ├── types/                 # TypeScript类型定义
│   │   ├── character.ts
│   │   ├── event.ts
│   │   ├── user.ts
│   │   └── world.ts
│   └── utils/                 # 工具函数
│       ├── platform.ts        # 跨端适配
│       └── storage.ts         # 本地存储封装
├── config/
│   └── dev.ts / prod.ts       # 环境配置
└── package.json
```

### 7.2 后端项目结构

```
server/
├── app/
│   ├── main.py                # FastAPI入口
│   ├── config.py              # 环境配置（pydantic-settings）
│   ├── api/                   # API层（Controllers）
│   │   ├── v1/
│   │   │   ├── auth.py
│   │   │   ├── characters.py
│   │   │   ├── events.py
│   │   │   └── world.py
│   │   └── deps.py            # 依赖注入
│   ├── domain/                # 领域层（纯业务逻辑）
│   │   ├── entities/          # 领域实体
│   │   │   ├── user.py
│   │   │   ├── character.py
│   │   │   ├── event.py
│   │   │   └── world.py
│   │   ├── services/          # 领域服务
│   │   │   ├── game_engine.py
│   │   │   ├── rule_engine.py
│   │   │   ├── time_service.py
│   │   │   └── event_service.py
│   │   └── interfaces/        # 领域接口（抽象）
│   │       ├── repository.py
│   │       └── event_generator.py
│   ├── infrastructure/        # 基础设施层
│   │   ├── database/          # 数据库
│   │   │   ├── connection.py
│   │   │   ├── models.py      # SQLAlchemy模型
│   │   │   └── migrations/    # Alembic迁移
│   │   ├── repositories/      # Repository实现
│   │   │   ├── user_repo.py
│   │   │   ├── character_repo.py
│   │   │   └── event_repo.py
│   │   ├── cache/             # Redis缓存
│   │   │   └── redis_client.py
│   │   └── tasks/             # Celery异步任务
│   │       └── game_tasks.py
│   └── schemas/               # Pydantic模型（请求/响应）
│       ├── auth.py
│       ├── character.py
│       ├── event.py
│       └── world.py
├── tests/                     # 测试
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── alembic.ini
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## 8. 跨端适配策略

### 8.1 微信小程序
- 主包 < 4MB，分包各 < 2MB
- 美术资源通过CDN远程加载
- 使用Taro小程序API适配层
- 微信登录 + 手机号绑定

### 8.2 H5/Web
- 响应式布局，适配桌面和移动浏览器
- 使用标准Web API
- 支持账号密码/手机号登录

### 8.3 React Native (安卓/iOS)
- Taro RN编译目标
- 原生导航和交互
- 推送通知支持
- 应用商店发布

### 8.4 统一账号体系
- 微信openid + unionid关联
- 手机号作为跨端唯一标识
- JWT Token认证，refresh token续期
- 数据完全云端同步，切换设备无感知

## 9. 后续迭代规划（不在MVP范围）

| 迭代 | 功能 | 优先级 |
|------|------|--------|
| V1.1 | 社交系统（好友互访、排行榜、分享） | 高 |
| V1.2 | AI事件生成（接入大模型） | 高 |
| V1.3 | 世界演变系统（时代变迁、大事件） | 中 |
| V2.0 | 3D地球渲染 | 中 |
| V2.1 | NPC行为AI | 低 |
| V2.2 | 角色人生轨迹分享（生成海报/视频） | 中 |
