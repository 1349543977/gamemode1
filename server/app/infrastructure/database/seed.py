"""种子数据：初始城市、职业、事件数据"""
from sqlalchemy.orm import Session
from app.infrastructure.database.models import CityModel, JobModel, EventModel, EventResultModel, WorldStateModel


def seed_cities(db: Session) -> None:
    cities = [
        CityModel(name="北京", region="华北", population=21540000, development_index=0.95, cost_of_living=0.9),
        CityModel(name="上海", region="华东", population=24870000, development_index=0.95, cost_of_living=0.92),
        CityModel(name="广州", region="华南", population=18680000, development_index=0.88, cost_of_living=0.75),
        CityModel(name="深圳", region="华南", population=17560000, development_index=0.92, cost_of_living=0.85),
        CityModel(name="成都", region="西南", population=20940000, development_index=0.78, cost_of_living=0.6),
        CityModel(name="杭州", region="华东", population=11940000, development_index=0.85, cost_of_living=0.72),
        CityModel(name="武汉", region="华中", population=12327000, development_index=0.75, cost_of_living=0.58),
        CityModel(name="西安", region="西北", population=12953000, development_index=0.7, cost_of_living=0.55),
        CityModel(name="南京", region="华东", population=9314000, development_index=0.82, cost_of_living=0.68),
        CityModel(name="重庆", region="西南", population=32054000, development_index=0.72, cost_of_living=0.52),
    ]
    db.add_all(cities)
    db.commit()


def seed_jobs(db: Session) -> None:
    jobs = [
        JobModel(name="程序员", category="科技", min_intelligence=60, min_charisma=30, salary_range={"min": 8000, "max": 35000}, stress_level=70, health_impact=-5),
        JobModel(name="教师", category="教育", min_intelligence=55, min_charisma=50, salary_range={"min": 5000, "max": 12000}, stress_level=55, health_impact=-2),
        JobModel(name="医生", category="医疗", min_intelligence=70, min_charisma=40, salary_range={"min": 8000, "max": 30000}, stress_level=80, health_impact=-8),
        JobModel(name="公务员", category="政府", min_intelligence=50, min_charisma=45, salary_range={"min": 6000, "max": 15000}, stress_level=40, health_impact=0),
        JobModel(name="销售", category="商业", min_intelligence=35, min_charisma=65, salary_range={"min": 4000, "max": 20000}, stress_level=65, health_impact=-3),
        JobModel(name="工人", category="制造", min_intelligence=25, min_charisma=20, salary_range={"min": 4000, "max": 8000}, stress_level=50, health_impact=-10),
        JobModel(name="艺术家", category="文化", min_intelligence=45, min_charisma=60, salary_range={"min": 3000, "max": 50000}, stress_level=60, health_impact=-2),
        JobModel(name="厨师", category="餐饮", min_intelligence=30, min_charisma=35, salary_range={"min": 4000, "max": 15000}, stress_level=60, health_impact=-5),
        JobModel(name="律师", category="法律", min_intelligence=65, min_charisma=55, salary_range={"min": 8000, "max": 40000}, stress_level=75, health_impact=-5),
        JobModel(name="创业者", category="商业", min_intelligence=55, min_charisma=60, salary_range={"min": 0, "max": 100000}, stress_level=90, health_impact=-10),
    ]
    db.add_all(jobs)
    db.commit()


def seed_events(db: Session) -> None:
    events_data = [
        {
            "event": EventModel(title="入学第一天", description="你背着新书包走进了小学的校门，一切都是那么新鲜。", stage="childhood", category="milestone", trigger_condition={"min_age": 7, "max_age": 7}, probability=1.0),
            "results": [
                EventResultModel(choice_text="认真听讲，做个好学生", choice_index=0, effects={"intelligence": 5, "happiness": -2}, narrative="你认真听讲，老师很快就注意到了你，让你当了小组长。"),
                EventResultModel(choice_text="和同学们打成一片", choice_index=1, effects={"charisma": 5, "happiness": 3}, narrative="你很快就交到了一群好朋友，课间总是最热闹的那个。"),
                EventResultModel(choice_text="对一切都感到害怕", choice_index=2, effects={"happiness": -5, "intelligence": 2}, narrative="你躲在角落里不敢说话，但默默观察着一切。"),
            ]
        },
        {
            "event": EventModel(title="中考来了", description="初中三年转瞬即逝，中考的成绩将决定你能否进入重点高中。", stage="adolescence", category="milestone", trigger_condition={"min_age": 15, "max_age": 15, "stats": {"intelligence": 40}}, probability=1.0),
            "results": [
                EventResultModel(choice_text="全力以赴冲刺", choice_index=0, effects={"intelligence": 8, "health": -3, "happiness": -5}, narrative="你拼尽全力复习，虽然过程辛苦，但最终考上了重点高中！"),
                EventResultModel(choice_text="正常发挥就好", choice_index=1, effects={"intelligence": 3, "happiness": 2}, narrative="你保持平常心，发挥稳定，进入了一所普通高中。"),
                EventResultModel(choice_text="不想考了", choice_index=2, effects={"intelligence": -3, "wealth": -5, "happiness": -8}, narrative="你放弃了努力，成绩不理想，只能去一所职业学校。"),
            ]
        },
        {
            "event": EventModel(title="初恋", description="你注意到班上有一个同学，每次看到对方你的心都会怦怦跳。", stage="adolescence", category="social", trigger_condition={"min_age": 14, "max_age": 18, "stats": {"charisma": 35}}, probability=0.6),
            "results": [
                EventResultModel(choice_text="鼓起勇气表白", choice_index=0, effects={"charisma": 5, "happiness": 8, "luck": -2}, narrative="你鼓起勇气表白了，对方红着脸点了点头，你的世界突然变得五彩斑斓。"),
                EventResultModel(choice_text="默默暗恋就好", choice_index=1, effects={"happiness": -3, "intelligence": 2}, narrative="你把这份感情藏在心底，化作了学习的动力。"),
                EventResultModel(choice_text="专注学习，不想这些", choice_index=2, effects={"intelligence": 5, "charisma": -3}, narrative="你强迫自己不去想这些，把精力都放在了书本上。"),
            ]
        },
        {
            "event": EventModel(title="高考", description="十二年寒窗苦读，高考就在眼前。这是改变命运的时刻。", stage="youth", category="milestone", trigger_condition={"min_age": 18, "max_age": 18}, probability=1.0),
            "results": [
                EventResultModel(choice_text="超常发挥", choice_index=0, effects={"intelligence": 10, "happiness": 10, "luck": 5}, narrative="你超常发挥，考出了远超预期的成绩，名校向你敞开了大门！"),
                EventResultModel(choice_text="正常发挥", choice_index=1, effects={"intelligence": 3, "happiness": 2}, narrative="你发挥正常，考上了一所不错的大学。"),
                EventResultModel(choice_text="发挥失常", choice_index=2, effects={"intelligence": -5, "happiness": -10, "luck": -5}, narrative="紧张让你发挥失常，成绩远不如平时，只能选择复读或去一所普通学校。"),
            ]
        },
        {
            "event": EventModel(title="求职面试", description="毕业了，你拿到了一家公司的面试通知。", stage="youth", category="career", trigger_condition={"min_age": 22, "max_age": 25}, probability=0.8),
            "results": [
                EventResultModel(choice_text="精心准备，自信应对", choice_index=0, effects={"wealth": 5, "intelligence": 2, "happiness": 3}, narrative="你准备充分，面试表现出色，顺利拿到了offer！"),
                EventResultModel(choice_text="紧张但努力表现", choice_index=1, effects={"wealth": 2, "happiness": -1}, narrative="虽然有些紧张，但你还是通过了面试，拿到了一份普通的工作。"),
                EventResultModel(choice_text="觉得不合适，放弃面试", choice_index=2, effects={"wealth": -5, "happiness": -3}, narrative="你放弃了这次机会，继续寻找更合适的方向。"),
            ]
        },
        {
            "event": EventModel(title="体检异常", description="年度体检报告出来了，有几项指标亮了红灯。", stage="prime", category="health", trigger_condition={"min_age": 35, "max_age": 55, "stats": {"health": 50}}, probability=0.5),
            "results": [
                EventResultModel(choice_text="立即就医，调整生活方式", choice_index=0, effects={"health": 5, "wealth": -5, "happiness": -2}, narrative="你开始规律作息、健康饮食，身体逐渐好转。"),
                EventResultModel(choice_text="太忙了，以后再说", choice_index=1, effects={"health": -10, "wealth": 2}, narrative="你继续忙碌的工作，身体状况越来越差。"),
            ]
        },
        {
            "event": EventModel(title="创业机会", description="一个朋友邀请你一起创业，这是一个风险与机遇并存的选择。", stage="prime", category="career", trigger_condition={"min_age": 28, "max_age": 45, "stats": {"intelligence": 50, "charisma": 45}}, probability=0.3),
            "results": [
                EventResultModel(choice_text="全力以赴，辞职创业", choice_index=0, effects={"wealth": -10, "happiness": 5, "health": -5, "luck": 10}, narrative="你辞去了稳定的工作，全身心投入创业。前路未知，但你充满激情。"),
                EventResultModel(choice_text="兼职尝试，稳中求进", choice_index=1, effects={"wealth": -3, "health": -3, "intelligence": 3}, narrative="你在工作之余尝试创业，虽然进展缓慢，但风险可控。"),
                EventResultModel(choice_text="婉拒邀请，保持稳定", choice_index=2, effects={"happiness": -3, "wealth": 2}, narrative="你选择了稳定的生活，但心里总觉得少了些什么。"),
            ]
        },
        {
            "event": EventModel(title="退休生活", description="到了退休的年纪，你终于可以放下工作了。", stage="elderly", category="milestone", trigger_condition={"min_age": 60, "max_age": 65}, probability=1.0),
            "results": [
                EventResultModel(choice_text="环游世界，享受人生", choice_index=0, effects={"happiness": 10, "wealth": -8, "health": -2}, narrative="你开始了环球旅行，看遍了大好河山，人生无憾。"),
                EventResultModel(choice_text="含饴弄孙，安享天伦", choice_index=1, effects={"happiness": 8, "health": 2}, narrative="你在家陪伴孙辈成长，享受着天伦之乐。"),
                EventResultModel(choice_text="发挥余热，继续工作", choice_index=2, effects={"wealth": 5, "health": -5, "happiness": -3}, narrative="你闲不住，继续做一些力所能及的工作。"),
            ]
        },
    ]

    for item in events_data:
        event = item["event"]
        db.add(event)
        db.flush()
        for result in item["results"]:
            result.event_id = event.id
            db.add(result)
    db.commit()


def seed_world_states(db: Session) -> None:
    state = WorldStateModel(year=2000, era="信息时代", gdp_index=0.5, tech_level=5, major_events=["互联网普及"])
    db.add(state)
    db.commit()


def run_all_seeds(db: Session) -> None:
    seed_cities(db)
    seed_jobs(db)
    seed_events(db)
    seed_world_states(db)
    print("Seed data inserted successfully")
