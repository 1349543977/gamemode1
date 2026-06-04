# 虚拟现实人生养成游戏 - 前端 MVP 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建人生养成游戏前端MVP，支持微信小程序/H5/React Native三端，实现角色创建、主游戏页、事件交互和年度总结核心流程。

**Architecture:** Taro 4 + React 18 + TypeScript，Zustand管理客户端状态，TanStack Query管理服务端状态，NutUI组件库，移动端优先响应式设计。

**Tech Stack:** Taro 4.x, React 18, TypeScript 5, Zustand, TanStack Query, NutUI (Taro版), ECharts (雷达图)

---

## 文件结构映射

```
client/
├── src/
│   ├── app.config.ts                # Taro应用配置（含分包）
│   ├── app.tsx                      # 入口
│   ├── app.scss                     # 全局样式
│   ├── styles/
│   │   ├── tokens.ts                # Design tokens
│   │   ├── dark-mode.scss           # 深色模式
│   │   └── global.scss              # 全局样式
│   ├── components/
│   │   ├── AttributeRadar/          # 属性雷达图
│   │   │   ├── index.tsx
│   │   │   └── index.scss
│   │   ├── EventCard/               # 事件卡片
│   │   │   ├── index.tsx
│   │   │   └── index.scss
│   │   ├── CharacterCard/           # 角色卡片
│   │   │   ├── index.tsx
│   │   │   └── index.scss
│   │   ├── YearSummaryModal/        # 年度总结弹窗
│   │   │   ├── index.tsx
│   │   │   └── index.scss
│   │   └── LoadingButton/           # 带loading的按钮
│   │       ├── index.tsx
│   │       └── index.scss
│   ├── pages/
│   │   ├── index/                   # 首页/角色列表
│   │   │   ├── index.tsx
│   │   │   └── index.scss
│   │   ├── login/                   # 登录页
│   │   │   ├── index.tsx
│   │   │   └── index.scss
│   │   ├── character-create/        # 角色创建
│   │   │   ├── index.tsx
│   │   │   └── index.scss
│   │   ├── game/                    # 主游戏页
│   │   │   ├── index.tsx
│   │   │   ├── index.scss
│   │   │   ├── MapTab.tsx
│   │   │   ├── StatsTab.tsx
│   │   │   ├── RecordsTab.tsx
│   │   │   └── SettingsTab.tsx
│   │   └── year-summary/            # 年度总结页
│   │       ├── index.tsx
│   │       └── index.scss
│   ├── stores/
│   │   ├── useAuthStore.ts
│   │   ├── useGameStore.ts
│   │   └── useCharacterStore.ts
│   ├── services/
│   │   ├── request.ts               # HTTP请求封装
│   │   ├── auth.ts
│   │   ├── character.ts
│   │   ├── event.ts
│   │   └── world.ts
│   ├── hooks/
│   │   ├── useTheme.ts
│   │   └── useLoading.ts
│   ├── types/
│   │   ├── character.ts
│   │   ├── event.ts
│   │   ├── user.ts
│   │   └── world.ts
│   └── utils/
│       ├── platform.ts
│       └── storage.ts
├── config/
│   ├── dev.ts
│   └── prod.ts
├── project.config.json              # 微信小程序配置
├── package.json
└── tsconfig.json
```

---

### Task 1: Taro项目初始化

**Files:**
- Create: `client/` 整个Taro项目
- Create: `client/src/app.config.ts`
- Create: `client/src/app.tsx`
- Create: `client/src/app.scss`
- Create: `client/package.json`
- Create: `client/tsconfig.json`
- Create: `client/project.config.json`

- [ ] **Step 1: 使用Taro CLI初始化项目**

Run: `cd /workspace && npx @tarojs/cli init client --template default --typescript --css scss 2>&1 | tail -10`
Expected: 项目创建成功

如果CLI不可用，手动创建项目结构。

- [ ] **Step 2: 安装依赖**

Run: `cd /workspace/client && npm install @tarojs/cli @tarojs/taro @tarojs/components @tarojs/runtime @tarojs/plugin-framework-react react react-dom zustand @tanstack/react-query nutui-taro @nutui/icons-react-taro 2>&1 | tail -5`

- [ ] **Step 3: 配置app.config.ts**

`client/src/app.config.ts`:
```typescript
export default defineAppConfig({
  pages: [
    'pages/index/index',
    'pages/login/index',
    'pages/character-create/index',
    'pages/game/index',
    'pages/year-summary/index',
  ],
  subPackages: [
    {
      root: 'packageGame',
      pages: [],
    },
  ],
  window: {
    backgroundTextStyle: 'light',
    navigationBarBackgroundColor: '#6366F1',
    navigationBarTitleText: '人生模拟器',
    navigationBarTextStyle: 'white',
  },
  tabBar: undefined,
});
```

- [ ] **Step 4: 创建入口文件**

`client/src/app.tsx`:
```typescript
import { PropsWithChildren } from 'react';
import './app.scss';

function App({ children }: PropsWithChildren) {
  return children;
}

export default App;
```

`client/src/app.scss`:
```scss
@import './styles/global.scss';
```

- [ ] **Step 5: 创建TypeScript配置**

`client/tsconfig.json`:
```json
{
  "compilerOptions": {
    "target": "ES2017",
    "module": "commonjs",
    "removeComments": false,
    "preserveConstEnums": true,
    "moduleResolution": "node",
    "experimentalDecorators": true,
    "noImplicitAny": false,
    "allowSyntheticDefaultImports": true,
    "outDir": "lib",
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "strictNullChecks": true,
    "sourceMap": true,
    "rootDir": ".",
    "jsx": "react-jsx",
    "allowJs": true,
    "resolveJsonModule": true,
    "typeRoots": ["node_modules/@types"],
    "paths": {
      "@/*": ["./src/*"]
    },
    "baseUrl": "."
  },
  "include": ["./src", "./types", "./config"],
  "compileOnSave": false
}
```

- [ ] **Step 6: 创建微信小程序项目配置**

`client/project.config.json`:
```json
{
  "miniprogramRoot": "dist/",
  "projectname": "life-simulation",
  "description": "虚拟现实人生养成游戏",
  "appid": "touristappid",
  "setting": {
    "urlCheck": false,
    "es6": false,
    "enhance": false,
    "compileHotReLoad": false,
    "postcss": false,
    "minified": false,
    "bundle": false
  },
  "compileType": "miniprogram"
}
```

- [ ] **Step 7: 验证项目可编译**

Run: `cd /workspace/client && npx taro build --type weapp 2>&1 | tail -5`
Expected: Build successful (可能有警告但不应有错误)

- [ ] **Step 8: Commit**

```bash
git add client/
git commit -m "feat(client): initialize Taro project with React + TypeScript"
```

---

### Task 2: Design Tokens与全局样式

**Files:**
- Create: `client/src/styles/tokens.ts`
- Create: `client/src/styles/global.scss`
- Create: `client/src/styles/dark-mode.scss`

- [ ] **Step 1: 创建Design Tokens**

`client/src/styles/tokens.ts`:
```typescript
export const tokens = {
  color: {
    primary: '#6366F1',
    primaryLight: '#818CF8',
    primaryDark: '#4F46E5',
    secondary: '#8B5CF6',
    success: '#10B981',
    warning: '#F59E0B',
    danger: '#EF4444',
    info: '#3B82F6',
    background: '#FFFFFF',
    surface: '#F8FAFC',
    surfaceVariant: '#F1F5F9',
    text: '#1E293B',
    textSecondary: '#64748B',
    textDisabled: '#94A3B8',
    border: '#E2E8F0',
    divider: '#F1F5F9',
  },
  darkColor: {
    primary: '#818CF8',
    primaryLight: '#A5B4FC',
    primaryDark: '#6366F1',
    secondary: '#A78BFA',
    background: '#0F172A',
    surface: '#1E293B',
    surfaceVariant: '#334155',
    text: '#F1F5F9',
    textSecondary: '#94A3B8',
    textDisabled: '#64748B',
    border: '#334155',
    divider: '#1E293B',
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
    xxl: '48px',
  },
  fontSize: {
    xs: '12px',
    sm: '14px',
    md: '16px',
    lg: '20px',
    xl: '24px',
    xxl: '32px',
    xxxl: '40px',
  },
  radius: {
    sm: '4px',
    md: '8px',
    lg: '12px',
    xl: '16px',
    xxl: '24px',
    full: '9999px',
  },
  shadow: {
    sm: '0 1px 2px rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
  },
} as const;

export type ThemeTokens = typeof tokens.color;
```

- [ ] **Step 2: 创建全局样式**

`client/src/styles/global.scss`:
```scss
@import './dark-mode.scss';

// CSS Variables for theming
:root {
  --color-primary: #6366F1;
  --color-primary-light: #818CF8;
  --color-secondary: #8B5CF6;
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-danger: #EF4444;
  --color-background: #FFFFFF;
  --color-surface: #F8FAFC;
  --color-surface-variant: #F1F5F9;
  --color-text: #1E293B;
  --color-text-secondary: #64748B;
  --color-text-disabled: #94A3B8;
  --color-border: #E2E8F0;

  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;

  --font-xs: 12px;
  --font-sm: 14px;
  --font-md: 16px;
  --font-lg: 20px;
  --font-xl: 24px;

  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;
}

// Reset
page {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: var(--font-md);
  color: var(--color-text);
  background-color: var(--color-background);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

// Utility classes
.container {
  padding: var(--spacing-md);
}

.text-center {
  text-align: center;
}

.text-primary {
  color: var(--color-primary);
}

.text-secondary {
  color: var(--color-text-secondary);
}

.text-danger {
  color: var(--color-danger);
}

.text-success {
  color: var(--color-success);
}

.flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

.flex-between {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.mt-sm { margin-top: var(--spacing-sm); }
.mt-md { margin-top: var(--spacing-md); }
.mt-lg { margin-top: var(--spacing-lg); }
.mb-sm { margin-bottom: var(--spacing-sm); }
.mb-md { margin-bottom: var(--spacing-md); }
.mb-lg { margin-bottom: var(--spacing-lg); }
```

- [ ] **Step 3: 创建深色模式样式**

`client/src/styles/dark-mode.scss`:
```scss
@media (prefers-color-scheme: dark) {
  :root {
    --color-primary: #818CF8;
    --color-primary-light: #A5B4FC;
    --color-secondary: #A78BFA;
    --color-background: #0F172A;
    --color-surface: #1E293B;
    --color-surface-variant: #334155;
    --color-text: #F1F5F9;
    --color-text-secondary: #94A3B8;
    --color-text-disabled: #64748B;
    --color-border: #334155;
  }
}

// Manual dark mode class
.dark-mode {
  --color-primary: #818CF8;
  --color-primary-light: #A5B4FC;
  --color-secondary: #A78BFA;
  --color-background: #0F172A;
  --color-surface: #1E293B;
  --color-surface-variant: #334155;
  --color-text: #F1F5F9;
  --color-text-secondary: #94A3B8;
  --color-text-disabled: #64748B;
  --color-border: #334155;
}
```

- [ ] **Step 4: Commit**

```bash
git add client/
git commit -m "feat(client): add design tokens, global styles, and dark mode support"
```

---

### Task 3: TypeScript类型定义与API服务层

**Files:**
- Create: `client/src/types/user.ts`
- Create: `client/src/types/character.ts`
- Create: `client/src/types/event.ts`
- Create: `client/src/types/world.ts`
- Create: `client/src/services/request.ts`
- Create: `client/src/services/auth.ts`
- Create: `client/src/services/character.ts`
- Create: `client/src/services/event.ts`
- Create: `client/src/services/world.ts`
- Create: `client/src/utils/storage.ts`
- Create: `client/src/utils/platform.ts`

- [ ] **Step 1: 创建类型定义**

`client/src/types/user.ts`:
```typescript
export interface User {
  id: number;
  nickname: string;
  avatar_url: string | null;
  phone: string | null;
  platform: string;
  has_phone: boolean;
}

export interface LoginRequest {
  code: string;
  platform: 'wechat' | 'ios' | 'android';
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

export interface PhoneBindRequest {
  phone: string;
  verify_code: string;
}
```

`client/src/types/character.ts`:
```typescript
export interface CharacterStats {
  health: number;
  intelligence: number;
  charisma: number;
  wealth: number;
  happiness: number;
  luck: number;
}

export interface Character {
  id: number;
  name: string;
  gender: 'male' | 'female';
  age: number;
  stage: string;
  is_alive: boolean;
  city: { id: number; name: string } | null;
  stats: CharacterStats | null;
}

export interface CreateCharacterRequest {
  name: string;
  gender: 'male' | 'female';
  city_id: number;
}

export interface LifeRecord {
  id: number;
  age: number;
  year: number;
  summary: string;
  stat_changes: Record<string, number> | null;
}

export interface AdvanceYearResponse {
  character: {
    age: number;
    stage: string;
    is_alive: boolean;
  };
  year_summary: {
    stat_changes: Record<string, number>;
    stage_changed: boolean;
    death_cause: string | null;
  };
  pending_events: PendingEvent[];
}

export interface PendingEvent {
  id: number;
  title: string;
  description: string;
  choices: { index: number; text: string }[];
}
```

`client/src/types/event.ts`:
```typescript
export interface EventChoiceRequest {
  character_id: number;
  choice_index: number;
}

export interface EventChoiceResult {
  narrative: string;
  effects: Record<string, number>;
  new_stats: {
    health: number;
    intelligence: number;
    charisma: number;
    wealth: number;
    happiness: number;
    luck: number;
  };
  triggered_events: { id: number; title: string; description: string }[];
}
```

`client/src/types/world.ts`:
```typescript
export interface City {
  id: number;
  name: string;
  region: string;
  population: number;
  development_index: number;
  cost_of_living: number;
}

export interface Job {
  id: number;
  name: string;
  category: string;
  min_intelligence: number;
  min_charisma: number;
  salary_range: { min: number; max: number };
  stress_level: number;
  health_impact: number;
}

export interface WorldState {
  year: number;
  era: string;
  gdp_index: number;
  tech_level: number;
  major_events: string[] | null;
}
```

- [ ] **Step 2: 创建HTTP请求封装**

`client/src/services/request.ts`:
```typescript
import Taro from '@tarojs/taro';
import { storage } from '../utils/storage';

const BASE_URL = process.env.TARO_APP_API_URL || 'http://localhost:8000/api/v1';

interface RequestOptions {
  url: string;
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  data?: unknown;
  header?: Record<string, string>;
}

class Request {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async getAuthHeader(): Promise<Record<string, string>> {
    const token = await storage.get('access_token');
    return token ? { Authorization: `Bearer ${token}` } : {};
  }

  async request<T>(options: RequestOptions): Promise<T> {
    const authHeader = await this.getAuthHeader();

    const response = await Taro.request({
      url: `${this.baseUrl}${options.url}`,
      method: options.method || 'GET',
      data: options.data,
      header: {
        'Content-Type': 'application/json',
        ...authHeader,
        ...options.header,
      },
    });

    if (response.statusCode === 401) {
      await storage.remove('access_token');
      Taro.redirectTo({ url: '/pages/login/index' });
      throw new Error('Unauthorized');
    }

    if (response.statusCode >= 400) {
      const error = response.data?.error?.message || response.data?.detail || 'Request failed';
      throw new Error(error);
    }

    return response.data as T;
  }

  get<T>(url: string) {
    return this.request<T>({ url, method: 'GET' });
  }

  post<T>(url: string, data?: unknown) {
    return this.request<T>({ url, method: 'POST', data });
  }

  put<T>(url: string, data?: unknown) {
    return this.request<T>({ url, method: 'PUT', data });
  }

  delete<T>(url: string) {
    return this.request<T>({ url, method: 'DELETE' });
  }
}

export const api = new Request(BASE_URL);
```

- [ ] **Step 3: 创建存储工具**

`client/src/utils/storage.ts`:
```typescript
import Taro from '@tarojs/taro';

export const storage = {
  async get(key: string): Promise<string | null> {
    try {
      const value = await Taro.getStorageSync(key);
      return value || null;
    } catch {
      return null;
    }
  },

  async set(key: string, value: string): Promise<void> {
    try {
      await Taro.setStorageSync(key, value);
    } catch (e) {
      console.error(`Failed to set storage key: ${key}`, e);
    }
  },

  async remove(key: string): Promise<void> {
    try {
      await Taro.removeStorageSync(key);
    } catch (e) {
      console.error(`Failed to remove storage key: ${key}`, e);
    }
  },
};
```

- [ ] **Step 4: 创建平台工具**

`client/src/utils/platform.ts`:
```typescript
import Taro from '@tarojs/taro';

export function getPlatform(): 'wechat' | 'ios' | 'android' | 'h5' {
  const env = Taro.getEnv();
  switch (env) {
    case Taro.ENV_TYPE.WEAPP:
      return 'wechat';
    case Taro.ENV_TYPE.WEB:
      return 'h5';
    case Taro.ENV_TYPE.RN:
      return 'ios'; // RN端需进一步判断
    default:
      return 'h5';
  }
}

export function isWeapp(): boolean {
  return Taro.getEnv() === Taro.ENV_TYPE.WEAPP;
}

export function navigateTo(url: string): void {
  Taro.navigateTo({ url });
}

export function redirectTo(url: string): void {
  Taro.redirectTo({ url });
}

export function switchTab(url: string): void {
  Taro.switchTab({ url });
}

export function showToast(title: string, icon: 'success' | 'error' | 'none' = 'none', duration = 1500): void {
  Taro.showToast({ title, icon, duration });
}

export function showLoading(title = '加载中...'): void {
  Taro.showLoading({ title, mask: true });
}

export function hideLoading(): void {
  Taro.hideLoading();
}
```

- [ ] **Step 5: 创建API服务**

`client/src/services/auth.ts`:
```typescript
import { api } from './request';
import type { LoginRequest, TokenResponse, PhoneBindRequest, User } from '../types/user';

export const authService = {
  wechatLogin(data: LoginRequest) {
    return api.post<TokenResponse>('/auth/wechat-login', data);
  },

  bindPhone(data: PhoneBindRequest) {
    return api.post<{ message: string; phone: string }>('/auth/phone-bind', data);
  },

  refreshToken(refreshToken: string) {
    return api.post<{ access_token: string; token_type: string }>('/auth/refresh', { refresh_token: refreshToken });
  },

  getProfile() {
    return api.get<User>('/auth/profile');
  },
};
```

`client/src/services/character.ts`:
```typescript
import { api } from './request';
import type { Character, CreateCharacterRequest, CharacterStats, LifeRecord, AdvanceYearResponse } from '../types/character';

export const characterService = {
  create(data: CreateCharacterRequest) {
    return api.post<Character>('/characters', data);
  },

  getById(id: number) {
    return api.get<Character>(`/characters/${id}`);
  },

  getStats(id: number) {
    return api.get<CharacterStats>(`/characters/${id}/stats`);
  },

  getLifeRecords(id: number, page = 1, pageSize = 20) {
    return api.get<{ records: LifeRecord[]; total: number }>(`/characters/${id}/life-records?page=${page}&page_size=${pageSize}`);
  },

  advanceYear(id: number) {
    return api.post<AdvanceYearResponse>(`/characters/${id}/advance`);
  },
};
```

`client/src/services/event.ts`:
```typescript
import { api } from './request';
import type { EventChoiceRequest, EventChoiceResult, PendingEvent } from '../types/event';

export const eventService = {
  getPendingEvents(characterId: number) {
    return api.get<PendingEvent[]>(`/events/pending/${characterId}`);
  },

  chooseOption(eventId: number, data: EventChoiceRequest) {
    return api.post<EventChoiceResult>(`/events/${eventId}/choose`, data);
  },
};
```

`client/src/services/world.ts`:
```typescript
import { api } from './request';
import type { City, Job, WorldState } from '../types/world';

export const worldService = {
  getWorldState() {
    return api.get<WorldState>('/world/state');
  },

  getCities() {
    return api.get<City[]>('/world/cities');
  },

  getJobs() {
    return api.get<Job[]>('/world/jobs');
  },
};
```

- [ ] **Step 6: Commit**

```bash
git add client/
git commit -m "feat(client): add TypeScript types, API services, and utility functions"
```

---

### Task 4: 状态管理 (Zustand Stores)

**Files:**
- Create: `client/src/stores/useAuthStore.ts`
- Create: `client/src/stores/useCharacterStore.ts`
- Create: `client/src/stores/useGameStore.ts`

- [ ] **Step 1: 创建认证Store**

`client/src/stores/useAuthStore.ts`:
```typescript
import { create } from 'zustand';
import type { User } from '../types/user';
import { storage } from '../utils/storage';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  setAuth: (user: User, token: string, refreshToken: string) => Promise<void>;
  logout: () => Promise<void>;
  loadFromStorage: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,

  setAuth: async (user, token, refreshToken) => {
    await storage.set('access_token', token);
    await storage.set('refresh_token', refreshToken);
    set({ user, token, isAuthenticated: true });
  },

  logout: async () => {
    await storage.remove('access_token');
    await storage.remove('refresh_token');
    set({ user: null, token: null, isAuthenticated: false });
  },

  loadFromStorage: async () => {
    const token = await storage.get('access_token');
    if (token) {
      set({ token, isAuthenticated: true });
    }
  },
}));
```

- [ ] **Step 2: 创建角色Store**

`client/src/stores/useCharacterStore.ts`:
```typescript
import { create } from 'zustand';
import type { Character, AdvanceYearResponse, PendingEvent } from '../types/character';

interface CharacterState {
  characters: Character[];
  currentCharacter: Character | null;
  pendingEvents: PendingEvent[];
  yearResult: AdvanceYearResponse | null;
  setCharacters: (characters: Character[]) => void;
  setCurrentCharacter: (character: Character | null) => void;
  setPendingEvents: (events: PendingEvent[]) => void;
  setYearResult: (result: AdvanceYearResponse | null) => void;
  removePendingEvent: (eventId: number) => void;
}

export const useCharacterStore = create<CharacterState>((set) => ({
  characters: [],
  currentCharacter: null,
  pendingEvents: [],
  yearResult: null,

  setCharacters: (characters) => set({ characters }),
  setCurrentCharacter: (character) => set({ currentCharacter: character }),
  setPendingEvents: (events) => set({ pendingEvents: events }),
  setYearResult: (result) => set({ yearResult: result }),
  removePendingEvent: (eventId) =>
    set((state) => ({
      pendingEvents: state.pendingEvents.filter((e) => e.id !== eventId),
    })),
}));
```

- [ ] **Step 3: 创建游戏Store**

`client/src/stores/useGameStore.ts`:
```typescript
import { create } from 'zustand';

interface GameState {
  isAdvancing: boolean;
  currentEventIndex: number;
  showYearSummary: boolean;
  darkMode: boolean;
  setIsAdvancing: (value: boolean) => void;
  setCurrentEventIndex: (index: number) => void;
  setShowYearSummary: (show: boolean) => void;
  toggleDarkMode: () => void;
  setDarkMode: (value: boolean) => void;
}

export const useGameStore = create<GameState>((set) => ({
  isAdvancing: false,
  currentEventIndex: 0,
  showYearSummary: false,
  darkMode: false,

  setIsAdvancing: (value) => set({ isAdvancing: value }),
  setCurrentEventIndex: (index) => set({ currentEventIndex: index }),
  setShowYearSummary: (show) => set({ showYearSummary: show }),
  toggleDarkMode: () => set((state) => ({ darkMode: !state.darkMode })),
  setDarkMode: (value) => set({ darkMode: value }),
}));
```

- [ ] **Step 4: Commit**

```bash
git add client/
git commit -m "feat(client): add Zustand stores for auth, character, and game state"
```

---

### Task 5: 通用组件

**Files:**
- Create: `client/src/components/LoadingButton/index.tsx`
- Create: `client/src/components/LoadingButton/index.scss`
- Create: `client/src/components/CharacterCard/index.tsx`
- Create: `client/src/components/CharacterCard/index.scss`
- Create: `client/src/components/EventCard/index.tsx`
- Create: `client/src/components/EventCard/index.scss`
- Create: `client/src/components/AttributeRadar/index.tsx`
- Create: `client/src/components/AttributeRadar/index.scss`
- Create: `client/src/components/YearSummaryModal/index.tsx`
- Create: `client/src/components/YearSummaryModal/index.scss`

- [ ] **Step 1: 创建LoadingButton组件**

`client/src/components/LoadingButton/index.tsx`:
```typescript
import { View, Text } from '@tarojs/components';
import { PropsWithChildren } from 'react';
import './index.scss';

interface LoadingButtonProps extends PropsWithChildren {
  loading?: boolean;
  disabled?: boolean;
  onClick?: () => void;
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
}

export default function LoadingButton({
  loading = false,
  disabled = false,
  onClick,
  children,
  variant = 'primary',
  size = 'md',
}: LoadingButtonProps) {
  return (
    <View
      className={`loading-btn loading-btn--${variant} loading-btn--${size} ${loading || disabled ? 'loading-btn--disabled' : ''}`}
      onClick={loading || disabled ? undefined : onClick}
    >
      {loading && <View className='loading-btn__spinner' />}
      <Text className='loading-btn__text'>{children}</Text>
    </View>
  );
}
```

`client/src/components/LoadingButton/index.scss`:
```scss
.loading-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-lg);
  font-weight: 600;
  transition: opacity 0.2s;

  &--primary {
    background: var(--color-primary);
    color: #fff;
  }

  &--secondary {
    background: var(--color-surface-variant);
    color: var(--color-text);
  }

  &--danger {
    background: var(--color-danger);
    color: #fff;
  }

  &--sm {
    padding: 8px 16px;
    font-size: var(--font-sm);
  }

  &--md {
    padding: 12px 24px;
    font-size: var(--font-md);
  }

  &--lg {
    padding: 16px 32px;
    font-size: var(--font-lg);
  }

  &--disabled {
    opacity: 0.6;
    pointer-events: none;
  }

  &__spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
    margin-right: 8px;
  }

  &__text {
    line-height: 1;
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

- [ ] **Step 2: 创建CharacterCard组件**

`client/src/components/CharacterCard/index.tsx`:
```typescript
import { View, Text } from '@tarojs/components';
import type { Character } from '../../types/character';
import './index.scss';

interface CharacterCardProps {
  character: Character;
  onClick?: (id: number) => void;
}

const STAGE_LABELS: Record<string, string> = {
  infant: '婴儿期',
  toddler: '幼儿期',
  childhood: '少年期',
  adolescence: '青春期',
  youth: '青年期',
  prime: '壮年期',
  middle_age: '中年期',
  elderly: '老年期',
};

export default function CharacterCard({ character, onClick }: CharacterCardProps) {
  return (
    <View className='character-card' onClick={() => onClick?.(character.id)}>
      <View className='character-card__header'>
        <Text className='character-card__name'>{character.name}</Text>
        <Text className={`character-card__status ${character.is_alive ? 'character-card__status--alive' : 'character-card__status--dead'}`}>
          {character.is_alive ? '存活' : '已故'}
        </Text>
      </View>
      <View className='character-card__info'>
        <Text className='character-card__age'>{character.age}岁</Text>
        <Text className='character-card__stage'>{STAGE_LABELS[character.stage] || character.stage}</Text>
        {character.city && <Text className='character-card__city'>{character.city.name}</Text>}
      </View>
      {character.stats && (
        <View className='character-card__stats'>
          <View className='stat-bar'>
            <Text className='stat-bar__label'>健康</Text>
            <View className='stat-bar__track'><View className='stat-bar__fill' style={{ width: `${character.stats.health}%`, background: 'var(--color-success)' }} /></View>
          </View>
          <View className='stat-bar'>
            <Text className='stat-bar__label'>智力</Text>
            <View className='stat-bar__track'><View className='stat-bar__fill' style={{ width: `${character.stats.intelligence}%`, background: 'var(--color-primary)' }} /></View>
          </View>
          <View className='stat-bar'>
            <Text className='stat-bar__label'>魅力</Text>
            <View className='stat-bar__track'><View className='stat-bar__fill' style={{ width: `${character.stats.charisma}%`, background: 'var(--color-secondary)' }} /></View>
          </View>
        </View>
      )}
    </View>
  );
}
```

`client/src/components/CharacterCard/index.scss`:
```scss
.character-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-md);
  box-shadow: var(--shadow-sm);

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-sm);
  }

  &__name {
    font-size: var(--font-lg);
    font-weight: 600;
    color: var(--color-text);
  }

  &__status {
    font-size: var(--font-xs);
    padding: 2px 8px;
    border-radius: var(--radius-full);

    &--alive {
      background: rgba(16, 185, 129, 0.1);
      color: var(--color-success);
    }

    &--dead {
      background: rgba(239, 68, 68, 0.1);
      color: var(--color-danger);
    }
  }

  &__info {
    display: flex;
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-sm);
  }

  &__age, &__stage, &__city {
    font-size: var(--font-sm);
    color: var(--color-text-secondary);
  }

  &__stats {
    margin-top: var(--spacing-sm);
  }
}

.stat-bar {
  display: flex;
  align-items: center;
  margin-bottom: 4px;

  &__label {
    width: 40px;
    font-size: var(--font-xs);
    color: var(--color-text-secondary);
  }

  &__track {
    flex: 1;
    height: 6px;
    background: var(--color-surface-variant);
    border-radius: 3px;
    overflow: hidden;
  }

  &__fill {
    height: 100%;
    border-radius: 3px;
    transition: width 0.3s ease;
  }
}
```

- [ ] **Step 3: 创建EventCard组件**

`client/src/components/EventCard/index.tsx`:
```typescript
import { View, Text } from '@tarojs/components';
import type { PendingEvent } from '../../types/character';
import LoadingButton from '../LoadingButton';
import './index.scss';

interface EventCardProps {
  event: PendingEvent;
  onChoose: (eventId: number, choiceIndex: number) => void;
  loading?: boolean;
}

export default function EventCard({ event, onChoose, loading = false }: EventCardProps) {
  return (
    <View className='event-card'>
      <View className='event-card__header'>
        <Text className='event-card__title'>{event.title}</Text>
      </View>
      <Text className='event-card__description'>{event.description}</Text>
      <View className='event-card__choices'>
        {event.choices.map((choice) => (
          <LoadingButton
            key={choice.index}
            variant='secondary'
            size='md'
            loading={loading}
            onClick={() => onChoose(event.id, choice.index)}
          >
            {choice.text}
          </LoadingButton>
        ))}
      </View>
    </View>
  );
}
```

`client/src/components/EventCard/index.scss`:
```scss
.event-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-md);
  box-shadow: var(--shadow-md);
  border-left: 4px solid var(--color-primary);

  &__header {
    margin-bottom: var(--spacing-sm);
  }

  &__title {
    font-size: var(--font-lg);
    font-weight: 700;
    color: var(--color-text);
  }

  &__description {
    font-size: var(--font-md);
    color: var(--color-text-secondary);
    line-height: 1.6;
    margin-bottom: var(--spacing-md);
  }

  &__choices {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-sm);
  }
}
```

- [ ] **Step 4: 创建AttributeRadar组件（简化版，用条形图替代）**

`client/src/components/AttributeRadar/index.tsx`:
```typescript
import { View, Text } from '@tarojs/components';
import type { CharacterStats } from '../../types/character';
import './index.scss';

interface AttributeRadarProps {
  stats: CharacterStats;
  showLabels?: boolean;
}

const STAT_CONFIG = [
  { key: 'health' as const, label: '健康', color: '#10B981' },
  { key: 'intelligence' as const, label: '智力', color: '#6366F1' },
  { key: 'charisma' as const, label: '魅力', color: '#8B5CF6' },
  { key: 'wealth' as const, label: '财富', color: '#F59E0B' },
  { key: 'happiness' as const, label: '幸福', color: '#EC4899' },
  { key: 'luck' as const, label: '运气', color: '#3B82F6' },
];

export default function AttributeRadar({ stats, showLabels = true }: AttributeRadarProps) {
  return (
    <View className='attribute-radar'>
      {STAT_CONFIG.map(({ key, label, color }) => (
        <View className='attribute-radar__row' key={key}>
          {showLabels && <Text className='attribute-radar__label'>{label}</Text>}
          <View className='attribute-radar__track'>
            <View
              className='attribute-radar__fill'
              style={{ width: `${stats[key]}%`, backgroundColor: color }}
            />
          </View>
          <Text className='attribute-radar__value'>{stats[key]}</Text>
        </View>
      ))}
    </View>
  );
}
```

`client/src/components/AttributeRadar/index.scss`:
```scss
.attribute-radar {
  padding: var(--spacing-md);

  &__row {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
  }

  &__label {
    width: 48px;
    font-size: var(--font-sm);
    color: var(--color-text-secondary);
    flex-shrink: 0;
  }

  &__track {
    flex: 1;
    height: 8px;
    background: var(--color-surface-variant);
    border-radius: 4px;
    overflow: hidden;
    margin: 0 var(--spacing-sm);
  }

  &__fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.5s ease;
  }

  &__value {
    width: 32px;
    text-align: right;
    font-size: var(--font-sm);
    font-weight: 600;
    color: var(--color-text);
    flex-shrink: 0;
  }
}
```

- [ ] **Step 5: 创建YearSummaryModal组件**

`client/src/components/YearSummaryModal/index.tsx`:
```typescript
import { View, Text } from '@tarojs/components';
import type { AdvanceYearResponse } from '../../types/character';
import LoadingButton from '../LoadingButton';
import './index.scss';

interface YearSummaryModalProps {
  result: AdvanceYearResponse;
  onClose: () => void;
}

const STAT_LABELS: Record<string, string> = {
  health: '健康',
  intelligence: '智力',
  charisma: '魅力',
  wealth: '财富',
  happiness: '幸福',
  luck: '运气',
};

export default function YearSummaryModal({ result, onClose }: YearSummaryModalProps) {
  const { character, year_summary } = result;

  return (
    <View className='year-summary'>
      <View className='year-summary__overlay' onClick={onClose} />
      <View className='year-summary__content'>
        <Text className='year-summary__title'>{character.age}岁年度总结</Text>

        {year_summary.stage_changed && (
          <View className='year-summary__milestone'>
            <Text className='year-summary__milestone-text'>人生进入新阶段！</Text>
          </View>
        )}

        <View className='year-summary__changes'>
          <Text className='year-summary__section-title'>属性变化</Text>
          {Object.entries(year_summary.stat_changes).map(([key, value]) => (
            <View className='year-summary__change-row' key={key}>
              <Text className='year-summary__change-label'>{STAT_LABELS[key] || key}</Text>
              <Text className={`year-summary__change-value ${value > 0 ? 'year-summary__change-value--up' : value < 0 ? 'year-summary__change-value--down' : ''}`}>
                {value > 0 ? `+${value}` : value}
              </Text>
            </View>
          ))}
        </View>

        {year_summary.death_cause && (
          <View className='year-summary__death'>
            <Text className='year-summary__death-text'>角色因"{year_summary.death_cause}"离世</Text>
          </View>
        )}

        <LoadingButton variant='primary' size='lg' onClick={onClose}>
          继续
        </LoadingButton>
      </View>
    </View>
  );
}
```

`client/src/components/YearSummaryModal/index.scss`:
```scss
.year-summary {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;

  &__overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
  }

  &__content {
    position: relative;
    background: var(--color-surface);
    border-radius: var(--radius-xl);
    padding: var(--spacing-xl);
    width: 85%;
    max-width: 400px;
  }

  &__title {
    font-size: var(--font-xl);
    font-weight: 700;
    color: var(--color-text);
    text-align: center;
    display: block;
    margin-bottom: var(--spacing-md);
  }

  &__milestone {
    background: rgba(99, 102, 241, 0.1);
    border-radius: var(--radius-md);
    padding: var(--spacing-sm) var(--spacing-md);
    margin-bottom: var(--spacing-md);
    text-align: center;
  }

  &__milestone-text {
    color: var(--color-primary);
    font-weight: 600;
  }

  &__section-title {
    font-size: var(--font-md);
    font-weight: 600;
    color: var(--color-text);
    display: block;
    margin-bottom: var(--spacing-sm);
  }

  &__change-row {
    display: flex;
    justify-content: space-between;
    padding: 4px 0;
  }

  &__change-label {
    color: var(--color-text-secondary);
  }

  &__change-value {
    font-weight: 600;

    &--up { color: var(--color-success); }
    &--down { color: var(--color-danger); }
  }

  &__death {
    background: rgba(239, 68, 68, 0.1);
    border-radius: var(--radius-md);
    padding: var(--spacing-md);
    margin-bottom: var(--spacing-md);
    text-align: center;
  }

  &__death-text {
    color: var(--color-danger);
    font-weight: 600;
  }
}
```

- [ ] **Step 6: Commit**

```bash
git add client/
git commit -m "feat(client): add LoadingButton, CharacterCard, EventCard, AttributeRadar, YearSummaryModal components"
```

---

### Task 6: 页面实现

**Files:**
- Create: `client/src/pages/login/index.tsx`
- Create: `client/src/pages/login/index.scss`
- Create: `client/src/pages/index/index.tsx`
- Create: `client/src/pages/index/index.scss`
- Create: `client/src/pages/character-create/index.tsx`
- Create: `client/src/pages/character-create/index.scss`
- Create: `client/src/pages/game/index.tsx`
- Create: `client/src/pages/game/index.scss`
- Create: `client/src/pages/game/StatsTab.tsx`
- Create: `client/src/pages/game/RecordsTab.tsx`
- Create: `client/src/pages/game/SettingsTab.tsx`

- [ ] **Step 1: 创建登录页**

`client/src/pages/login/index.tsx`:
```typescript
import { View, Text, Button } from '@tarojs/components';
import Taro from '@tarojs/taro';
import { useAuthStore } from '../../stores/useAuthStore';
import { authService } from '../../services/auth';
import { getPlatform } from '../../utils/platform';
import './index.scss';

export default function Login() {
  const setAuth = useAuthStore((s) => s.setAuth);

  const handleWechatLogin = async () => {
    try {
      const { code } = await Taro.login();
      const result = await authService.wechatLogin({
        code,
        platform: getPlatform() as 'wechat',
      });
      await setAuth(result.user, result.access_token, result.refresh_token);
      Taro.redirectTo({ url: '/pages/index/index' });
    } catch (e) {
      Taro.showToast({ title: '登录失败', icon: 'error' });
    }
  };

  return (
    <View className='login-page'>
      <View className='login-page__header'>
        <Text className='login-page__title'>人生模拟器</Text>
        <Text className='login-page__subtitle'>观察 · 引导 · 见证一生</Text>
      </View>
      <View className='login-page__actions'>
        <Button className='login-page__btn login-page__btn--wechat' onClick={handleWechatLogin}>
          微信一键登录
        </Button>
      </View>
    </View>
  );
}
```

`client/src/pages/login/index.scss`:
```scss
.login-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl);
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);

  &__header {
    text-align: center;
    margin-bottom: 80px;
  }

  &__title {
    font-size: 40px;
    font-weight: 800;
    color: #fff;
    display: block;
  }

  &__subtitle {
    font-size: var(--font-md);
    color: rgba(255, 255, 255, 0.8);
    display: block;
    margin-top: var(--spacing-sm);
  }

  &__actions {
    width: 100%;
    max-width: 320px;
  }

  &__btn {
    width: 100%;
    height: 48px;
    border-radius: var(--radius-lg);
    font-size: var(--font-md);
    font-weight: 600;
    border: none;

    &--wechat {
      background: #07C160;
      color: #fff;
    }
  }
}
```

- [ ] **Step 2: 创建首页（角色列表）**

`client/src/pages/index/index.tsx`:
```typescript
import { View, Text } from '@tarojs/components';
import Taro from '@tarojs/taro';
import { useEffect, useState } from 'react';
import { characterService } from '../../services/character';
import { useAuthStore } from '../../stores/useAuthStore';
import { useCharacterStore } from '../../stores/useCharacterStore';
import CharacterCard from '../../components/CharacterCard';
import LoadingButton from '../../components/LoadingButton';
import type { Character } from '../../types/character';
import './index.scss';

export default function Index() {
  const [loading, setLoading] = useState(true);
  const user = useAuthStore((s) => s.user);
  const { setCharacters, setCurrentCharacter } = useCharacterStore();
  const characters = useCharacterStore((s) => s.characters);

  useEffect(() => {
    loadCharacters();
  }, []);

  const loadCharacters = async () => {
    try {
      setLoading(true);
      // MVP: 直接获取所有角色（后续API需添加list端点）
      // const data = await characterService.list();
      setCharacters([]);
    } catch (e) {
      Taro.showToast({ title: '加载失败', icon: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const handleCharacterClick = (id: number) => {
    setCurrentCharacter(characters.find((c) => c.id === id) || null);
    Taro.navigateTo({ url: `/pages/game/index?characterId=${id}` });
  };

  const handleCreateNew = () => {
    Taro.navigateTo({ url: '/pages/character-create/index' });
  };

  return (
    <View className='index-page'>
      <View className='index-page__header'>
        <Text className='index-page__greeting'>你好，{user?.nickname || '玩家'}</Text>
        <Text className='index-page__subtitle'>选择一个角色开始人生</Text>
      </View>

      {loading ? (
        <View className='index-page__skeleton'>
          {[1, 2, 3].map((i) => (
            <View key={i} className='skeleton-card' />
          ))}
        </View>
      ) : (
        <View className='index-page__list'>
          {characters.map((char) => (
            <CharacterCard key={char.id} character={char} onClick={handleCharacterClick} />
          ))}
        </View>
      )}

      <View className='index-page__footer'>
        <LoadingButton variant='primary' size='lg' onClick={handleCreateNew}>
          创建新角色
        </LoadingButton>
      </View>
    </View>
  );
}
```

`client/src/pages/index/index.scss`:
```scss
.index-page {
  min-height: 100vh;
  padding: var(--spacing-md);
  background: var(--color-background);

  &__header {
    margin-bottom: var(--spacing-lg);
  }

  &__greeting {
    font-size: var(--font-xl);
    font-weight: 700;
    color: var(--color-text);
    display: block;
  }

  &__subtitle {
    font-size: var(--font-md);
    color: var(--color-text-secondary);
    display: block;
    margin-top: var(--spacing-xs);
  }

  &__skeleton {
    .skeleton-card {
      height: 120px;
      background: var(--color-surface-variant);
      border-radius: var(--radius-lg);
      margin-bottom: var(--spacing-md);
      animation: pulse 1.5s ease-in-out infinite;
    }
  }

  &__list {
    margin-bottom: 80px;
  }

  &__footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: var(--spacing-md);
    background: var(--color-background);
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
  }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
```

- [ ] **Step 3: 创建角色创建页**

`client/src/pages/character-create/index.tsx`:
```typescript
import { View, Text, Input, Picker } from '@tarojs/components';
import Taro from '@tarojs/taro';
import { useState, useEffect } from 'react';
import { characterService } from '../../services/character';
import { worldService } from '../../services/world';
import { useCharacterStore } from '../../stores/useCharacterStore';
import LoadingButton from '../../components/LoadingButton';
import type { City } from '../../types/world';
import './index.scss';

export default function CharacterCreate() {
  const [name, setName] = useState('');
  const [gender, setGender] = useState<'male' | 'female'>('male');
  const [cities, setCities] = useState<City[]>([]);
  const [selectedCity, setSelectedCity] = useState(0);
  const [creating, setCreating] = useState(false);

  const { setCharacters, setCurrentCharacter } = useCharacterStore();

  useEffect(() => {
    loadCities();
  }, []);

  const loadCities = async () => {
    try {
      const data = await worldService.getCities();
      setCities(data);
      if (data.length > 0) setSelectedCity(0);
    } catch (e) {
      Taro.showToast({ title: '加载城市失败', icon: 'error' });
    }
  };

  const handleCreate = async () => {
    if (!name.trim()) {
      Taro.showToast({ title: '请输入角色姓名', icon: 'none' });
      return;
    }
    if (cities.length === 0) {
      Taro.showToast({ title: '请选择出生城市', icon: 'none' });
      return;
    }

    try {
      setCreating(true);
      const character = await characterService.create({
        name: name.trim(),
        gender,
        city_id: cities[selectedCity].id,
      });
      setCurrentCharacter(character);
      Taro.redirectTo({ url: `/pages/game/index?characterId=${character.id}` });
    } catch (e) {
      Taro.showToast({ title: '创建失败', icon: 'error' });
    } finally {
      setCreating(false);
    }
  };

  const genderOptions = ['男', '女'];

  return (
    <View className='create-page'>
      <Text className='create-page__title'>创建新角色</Text>

      <View className='create-page__form'>
        <View className='form-field'>
          <Text className='form-field__label'>姓名</Text>
          <Input
            className='form-field__input'
            placeholder='给角色取个名字'
            value={name}
            onInput={(e) => setName(e.detail.value)}
            maxlength={20}
          />
        </View>

        <View className='form-field'>
          <Text className='form-field__label'>性别</Text>
          <Picker
            mode='selector'
            range={genderOptions}
            value={gender === 'male' ? 0 : 1}
            onChange={(e) => setGender(e.detail.value === 0 ? 'male' : 'female')}
          >
            <View className='form-field__picker'>{gender === 'male' ? '男' : '女'}</View>
          </Picker>
        </View>

        <View className='form-field'>
          <Text className='form-field__label'>出生城市</Text>
          <Picker
            mode='selector'
            range={cities.map((c) => c.name)}
            value={selectedCity}
            onChange={(e) => setSelectedCity(Number(e.detail.value))}
          >
            <View className='form-field__picker'>
              {cities[selectedCity]?.name || '选择城市'}
            </View>
          </Picker>
        </View>
      </View>

      <LoadingButton variant='primary' size='lg' loading={creating} onClick={handleCreate}>
        开始人生
      </LoadingButton>
    </View>
  );
}
```

`client/src/pages/character-create/index.scss`:
```scss
.create-page {
  min-height: 100vh;
  padding: var(--spacing-lg);
  background: var(--color-background);

  &__title {
    font-size: var(--font-xl);
    font-weight: 700;
    color: var(--color-text);
    display: block;
    margin-bottom: var(--spacing-xl);
  }

  &__form {
    margin-bottom: var(--spacing-xl);
  }
}

.form-field {
  margin-bottom: var(--spacing-lg);

  &__label {
    font-size: var(--font-md);
    font-weight: 600;
    color: var(--color-text);
    display: block;
    margin-bottom: var(--spacing-sm);
  }

  &__input {
    width: 100%;
    height: 48px;
    padding: 0 var(--spacing-md);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    font-size: var(--font-md);
    background: var(--color-surface);
    color: var(--color-text);
  }

  &__picker {
    height: 48px;
    line-height: 48px;
    padding: 0 var(--spacing-md);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    font-size: var(--font-md);
    background: var(--color-surface);
    color: var(--color-text);
  }
}
```

- [ ] **Step 4: 创建主游戏页**

`client/src/pages/game/index.tsx`:
```typescript
import { View, Text } from '@tarojs/components';
import Taro, { useRouter } from '@tarojs/taro';
import { useEffect, useState, useCallback } from 'react';
import { characterService } from '../../services/character';
import { eventService } from '../../services/event';
import { useCharacterStore } from '../../stores/useCharacterStore';
import { useGameStore } from '../../stores/useGameStore';
import AttributeRadar from '../../components/AttributeRadar';
import EventCard from '../../components/EventCard';
import YearSummaryModal from '../../components/YearSummaryModal';
import LoadingButton from '../../components/LoadingButton';
import './index.scss';

export default function Game() {
  const router = useRouter();
  const characterId = Number(router.params.characterId || 0);

  const currentCharacter = useCharacterStore((s) => s.currentCharacter);
  const setCurrentCharacter = useCharacterStore((s) => s.setCurrentCharacter);
  const pendingEvents = useCharacterStore((s) => s.pendingEvents);
  const setPendingEvents = useCharacterStore((s) => s.setPendingEvents);
  const yearResult = useCharacterStore((s) => s.yearResult);
  const setYearResult = useCharacterStore((s) => s.setYearResult);
  const removePendingEvent = useCharacterStore((s) => s.removePendingEvent);

  const isAdvancing = useGameStore((s) => s.isAdvancing);
  const setIsAdvancing = useGameStore((s) => s.setIsAdvancing);
  const showYearSummary = useGameStore((s) => s.showYearSummary);
  const setShowYearSummary = useGameStore((s) => s.setShowYearSummary);

  const [activeTab, setActiveTab] = useState<'map' | 'stats' | 'records' | 'settings'>('map');
  const [choosingEvent, setChoosingEvent] = useState(false);

  useEffect(() => {
    if (characterId) {
      loadCharacter();
    }
  }, [characterId]);

  const loadCharacter = async () => {
    try {
      const char = await characterService.getById(characterId);
      setCurrentCharacter(char);
    } catch (e) {
      Taro.showToast({ title: '加载失败', icon: 'error' });
    }
  };

  const handleAdvanceYear = useCallback(async () => {
    if (!characterId || isAdvancing) return;

    try {
      setIsAdvancing(true);
      const result = await characterService.advanceYear(characterId);
      setYearResult(result);
      setPendingEvents(result.pending_events);

      if (result.character.is_alive) {
        await loadCharacter();
      }

      if (result.pending_events.length === 0) {
        setShowYearSummary(true);
      }
    } catch (e) {
      Taro.showToast({ title: '推进失败', icon: 'error' });
    } finally {
      setIsAdvancing(false);
    }
  }, [characterId, isAdvancing]);

  const handleEventChoose = useCallback(async (eventId: number, choiceIndex: number) => {
    if (!characterId || choosingEvent) return;

    try {
      setChoosingEvent(true);
      const result = await eventService.chooseOption(eventId, {
        character_id: characterId,
        choice_index: choiceIndex,
      });

      removePendingEvent(eventId);
      await loadCharacter();

      if (pendingEvents.length <= 1) {
        setShowYearSummary(true);
      }
    } catch (e) {
      Taro.showToast({ title: '选择失败', icon: 'error' });
    } finally {
      setChoosingEvent(false);
    }
  }, [characterId, choosingEvent, pendingEvents.length]);

  const handleCloseSummary = useCallback(() => {
    setShowYearSummary(false);
    setYearResult(null);
  }, []);

  if (!currentCharacter) {
    return <View className='game-page'><Text>加载中...</Text></View>;
  }

  return (
    <View className='game-page'>
      {/* 角色信息栏 */}
      <View className='game-page__header'>
        <View className='game-page__char-info'>
          <Text className='game-page__char-name'>{currentCharacter.name}</Text>
          <Text className='game-page__char-age'>{currentCharacter.age}岁</Text>
        </View>
        <Text className='game-page__char-stage'>
          {getStageLabel(currentCharacter.stage)}
        </Text>
      </View>

      {/* 待处理事件 */}
      {pendingEvents.length > 0 && (
        <View className='game-page__events'>
          <Text className='game-page__events-title'>待处理事件</Text>
          {pendingEvents.map((event) => (
            <EventCard
              key={event.id}
              event={event}
              onChoose={handleEventChoose}
              loading={choosingEvent}
            />
          ))}
        </View>
      )}

      {/* Tab内容区 */}
      <View className='game-page__content'>
        {activeTab === 'map' && (
          <View className='game-page__map'>
            <Text className='game-page__map-placeholder'>
              {currentCharacter.city?.name || '未知城市'}
            </Text>
          </View>
        )}
        {activeTab === 'stats' && currentCharacter.stats && (
          <AttributeRadar stats={currentCharacter.stats} />
        )}
        {activeTab === 'records' && (
          <View className='game-page__records'>
            <Text className='text-secondary'>人生记录将在这里显示</Text>
          </View>
        )}
        {activeTab === 'settings' && (
          <View className='game-page__settings'>
            <Text className='text-secondary'>游戏设置</Text>
          </View>
        )}
      </View>

      {/* 底部操作栏 */}
      <View className='game-page__footer'>
        <View className='game-page__tabs'>
          {(['map', 'stats', 'records', 'settings'] as const).map((tab) => (
            <View
              key={tab}
              className={`game-page__tab ${activeTab === tab ? 'game-page__tab--active' : ''}`}
              onClick={() => setActiveTab(tab)}
            >
              <Text>{getTabLabel(tab)}</Text>
            </View>
          ))}
        </View>
        {currentCharacter.is_alive && pendingEvents.length === 0 && (
          <LoadingButton
            variant='primary'
            size='lg'
            loading={isAdvancing}
            onClick={handleAdvanceYear}
          >
            度过这一年
          </LoadingButton>
        )}
      </View>

      {/* 年度总结弹窗 */}
      {showYearSummary && yearResult && (
        <YearSummaryModal result={yearResult} onClose={handleCloseSummary} />
      )}
    </View>
  );
}

const STAGE_LABELS: Record<string, string> = {
  infant: '婴儿期', toddler: '幼儿期', childhood: '少年期',
  adolescence: '青春期', youth: '青年期', prime: '壮年期',
  middle_age: '中年期', elderly: '老年期',
};

function getStageLabel(stage: string): string {
  return STAGE_LABELS[stage] || stage;
}

function getTabLabel(tab: string): string {
  const map: Record<string, string> = { map: '地图', stats: '属性', records: '记录', settings: '设置' };
  return map[tab] || tab;
}
```

`client/src/pages/game/index.scss`:
```scss
.game-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-background);

  &__header {
    padding: var(--spacing-md);
    background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
    color: #fff;
  }

  &__char-info {
    display: flex;
    align-items: baseline;
    gap: var(--spacing-sm);
  }

  &__char-name {
    font-size: var(--font-xl);
    font-weight: 700;
  }

  &__char-age {
    font-size: var(--font-md);
    opacity: 0.9;
  }

  &__char-stage {
    font-size: var(--font-sm);
    opacity: 0.8;
    margin-top: var(--spacing-xs);
    display: block;
  }

  &__events {
    padding: var(--spacing-md);
  }

  &__events-title {
    font-size: var(--font-lg);
    font-weight: 600;
    color: var(--color-text);
    display: block;
    margin-bottom: var(--spacing-md);
  }

  &__content {
    flex: 1;
    padding: var(--spacing-md);
  }

  &__map {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 300px;
    background: var(--color-surface);
    border-radius: var(--radius-lg);
  }

  &__map-placeholder {
    font-size: var(--font-lg);
    color: var(--color-text-secondary);
  }

  &__footer {
    padding: var(--spacing-md);
    background: var(--color-surface);
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
  }

  &__tabs {
    display: flex;
    justify-content: space-around;
    margin-bottom: var(--spacing-md);
  }

  &__tab {
    padding: var(--spacing-sm) var(--spacing-md);
    font-size: var(--font-sm);
    color: var(--color-text-secondary);
    border-radius: var(--radius-md);

    &--active {
      background: var(--color-primary);
      color: #fff;
    }
  }
}
```

- [ ] **Step 5: Commit**

```bash
git add client/
git commit -m "feat(client): implement all pages - login, index, character-create, game"
```

---

### Task 7: 最终验证与构建

- [ ] **Step 1: 验证TypeScript编译**

Run: `cd /workspace/client && npx tsc --noEmit 2>&1 | tail -10`
Expected: No errors (可能有Taro相关的类型警告)

- [ ] **Step 2: 构建微信小程序版本**

Run: `cd /workspace/client && npx taro build --type weapp 2>&1 | tail -10`
Expected: Build successful

- [ ] **Step 3: 构建H5版本**

Run: `cd /workspace/client && npx taro build --type h5 2>&1 | tail -10`
Expected: Build successful

- [ ] **Step 4: Commit**

```bash
git add client/
git commit -m "feat(client): finalize with build verification for weapp and h5"
```
