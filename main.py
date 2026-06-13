# -*- coding: utf-8 -*-
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
from typing import Optional
from pydantic import BaseModel

app = FastAPI(title="Silver Back")

BASE_DIR = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TPL_DIR = os.path.join(BASE_DIR, "templates")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
jinja_env = Environment(loader=FileSystemLoader(TPL_DIR))

# --- 展示用教练数据 ---
coaches = [
    {"id":1,"name":"张教练","title":"主教练","badge":"NSCA-CSCS","years":"10年","desc":"省队体能教练出身，擅长力量训练与运动表现提升。带过3名国家级运动员，帮助超过200名普通训练者突破瓶颈。","tags":["力量训练","运动表现","周期化"],"students":200,"hours":8000,"ratio":"98%"},
    {"id":2,"name":"李教练","title":"高级教练","badge":"ACE-CPT","years":"8年","desc":"累计授课超10000节。专注减脂塑形与体态纠正，擅长把复杂的训练原理讲得简单易懂。","tags":["减脂塑形","体态纠正","营养规划"],"students":300,"hours":10000,"ratio":"95%"},
    {"id":3,"name":"王教练","title":"康复教练","badge":"NASM-CES","years":"6年","desc":"专注术后康复与慢性疼痛管理。曾任某三甲医院康复中心体能顾问，擅长用功能性训练解决疼痛问题。","tags":["康复训练","疼痛管理","功能性训练"],"students":150,"hours":6000,"ratio":"97%"},
]

# --- 会员蜕变故事 ---
transformations = [
    {"id":1,"name":"小雅","avatar":"👩","period":"3个月","from_data":"体脂 32%","to_data":"体脂 24%","weight_change":"−12斤","story":"从来不爱运动的办公室白领，从第一次卧推空杆都发抖，到能完成标准引体向上。她说最大的收获不是瘦了，是爱上了流汗的感觉。","tags":["减脂","塑形"],"highlight":"体脂下降8% · 引体向上突破"},
    {"id":2,"name":"阿杰","avatar":"👨","period":"6个月","from_data":"深蹲 40kg","to_data":"深蹲 120kg","weight_change":"＋10kg肌","story":"健身3年一直原地踏步，瓶颈期困扰了他整整一年。经过系统周期化训练和动作模式重建，半年实现成绩翻倍。","tags":["增肌","力量"],"highlight":"深蹲 40→120kg · 三大项突破300kg"},
    {"id":3,"name":"蕾蕾","avatar":"👩‍💼","period":"4个月","from_data":"腹直肌分离2指","to_data":"完全恢复","weight_change":"−8斤","story":"产后6个月来到工作室。从不敢做任何核心动作，到可以完成平板支撑2分钟，腹直肌分离完全闭合。","tags":["产后恢复","康复"],"highlight":"腹直肌闭合 · 核心力量重建"},
    {"id":4,"name":"老陈","avatar":"👨‍🦰","period":"8个月","from_data":"体脂 28%","to_data":"体脂 18%","weight_change":"−16斤","story":"45岁的中年企业家，体检报告亮红灯后下定决心。从最开始走15分钟都喘，到现在每周5练，体检指标全部恢复正常。","tags":["减脂","健康管理"],"highlight":"脂肪肝逆转 · 体检指标全正常"},
]

# --- 私教课价格 ---
pricing = [
    {"id":1,"name":"单次体验","sessions":1,"price":399,"unit_price":399,"tag":"体验","features":["1对1 专业指导","体态评估","训练计划制定"],"popular":False},
    {"id":2,"name":"10节私教","sessions":10,"price":3599,"unit_price":360,"tag":"入门","features":["1对1 专业指导","体态评估","训练计划制定","饮食建议","课后小结推送"],"popular":False},
    {"id":3,"name":"20节私教","sessions":20,"price":6399,"unit_price":320,"tag":"推荐","features":["1对1 专业指导","体态评估","训练计划制定","饮食建议","课后小结推送","月度体测","灵活约课"],"popular":True},
    {"id":4,"name":"40节私教","sessions":40,"price":11199,"unit_price":280,"tag":"超值","features":["1对1 专业指导","体态评估","训练计划制定","饮食建议","课后小结推送","月度体测","灵活约课","无限次自主训练"],"popular":False},
]

# --- 会员数据库（内存） ---
members_db = {
    "138****0001": {
        "phone":"138****0001","name":"小雅","avatar":"👩","member_since":"2025-09-01","total_sessions":28,"trainer":"李教练","trainer_phone":"13811111101",
        "records":[
            {"date":"2026-06-10","type":"力量训练","duration":"60min","content":"深蹲 5×5 @50kg\n卧推 4×8 @30kg\n划船 4×10 @25kg\n平板支撑 3×45s","mood":"💭 状态很好"},
            {"date":"2026-06-08","type":"体能训练","duration":"50min","content":"波比跳 10×3\n壶铃摆动 4×15 @16kg\n农夫行走 3×30m @24kg\n战绳 30s×5","mood":"😫 有点疲惫"},
        ]
    },
    "138****0002": {
        "phone":"138****0002","name":"阿杰","avatar":"👨","member_since":"2025-12-01","total_sessions":35,"trainer":"张教练","trainer_phone":"13811111102",
        "records":[
            {"date":"2026-06-11","type":"力量训练","duration":"90min","content":"深蹲 5×3 @100kg\n卧推 5×5 @70kg\n硬拉 3×3 @110kg","mood":"🔥 燃起来了"},
            {"date":"2026-06-09","type":"恢复训练","duration":"45min","content":"泡沫轴放松\n动态拉伸\n核心激活\n有氧 20min","mood":"😉 轻松完成"},
        ]
    },
    "138****0003": {
        "phone":"138****0003","name":"蕾蕾","avatar":"👩‍💼","member_since":"2026-01-15","total_sessions":18,"trainer":"李教练","trainer_phone":"13811111101",
        "records":[
            {"date":"2026-06-09","type":"康复训练","duration":"50min","content":"核心激活\n呼吸训练\n臀桥 4×15\n四足支撑 3×30s","mood":"😉 轻松完成"},
        ]
    },
}

# --- 教练账号 ---
coach_accounts = [
    {"id":1,"name":"张教练","avatar":"🏋️","badge":"NSCA-CSCS","phone":"138****1102","members":[
        {"phone":"138****0002","name":"阿杰","avatar":"👨","member_since":"2025-12-01","total_sessions":35},
    ]},
    {"id":2,"name":"李教练","avatar":"🏋️","badge":"ACE-CPT","phone":"138****1101","members":[
        {"phone":"138****0001","name":"小雅","avatar":"👩","member_since":"2025-09-01","total_sessions":28},
        {"phone":"138****0003","name":"蕾蕾","avatar":"👩‍💼","member_since":"2026-01-15","total_sessions":18},
    ]},
]

# --- 营养指南 ---
nutrition_guides = [
    {"id":1,"title":"什么是5:2轻断食？","content":"5:2轻断食是一种间歇性断食法。每周5天正常饮食，选择不连续2天进行低热量摄入（女性约500kcal，男性约600kcal）。研究表明5:2断食法对减脂、胰岝素敏感度提升和细胞自噬有显著效果。"},
    {"id":2,"title":"断食日怎么吃？","content":"断食日建议摄入高蛋白、高纤维的食物，如鸡胸肉、鱼虾、绿叶蔬菜、蛋类。避免精制碳水和含糖饮料。可以将热量分配到1-2餐中，根据个人习惯选择早餐+晚餐或仅午餐。"},
    {"id":3,"title":"非断食日注意事项","content":"非断食日不需要严格限制，但建议保持均衡营养。蛋白质摄入建议达到体重kg×1.2-1.6g，保证训练后营养补充。不建议在非断食日暴饮暴食。"},
    {"id":4,"title":"训练日与断食的搭配","content":"高强度训练日尽量安排在非断食日。若断食日有训练，建议训练前摄入少量快碳（如一根香蕉），训练后立即补充蛋白质。断食日适合进行低强度有氧或恢复性训练。"},
    {"id":5,"title":"适合哪些人群？","content":"5:2轻断食适合体重正常至超重的健康人群，尤其适合：减脂平台期、工作忙碌难以每日控制饮食者、想要改善代谢健康的人群。不建议孕妇、青少年、糖尿病患者、饮食失调史者使用。"},
    {"id":6,"title":"常见问题","content":"Q:断食日会很饿吗？\nA:通常2-3周后身体会适应，饥饿感明显下降。\n\nQ:可以喝咖啡和茶吗？\nA:可以，建议不加糖奶。黑咖啡和茶有助于抑制饥饿。\n\nQ:多久能看到效果？\nA:坚持4-6周可以看到明显体脂变化，配合训练效果更佳。"},
]

member_photos = {}
member_strength = {}
member_grip = {}
member_rpe = {}
member_meals = {}
coach_plans = {}
coach_extra_records = {}
_id_counter = [1000]

def next_id():
    _id_counter[0] += 1
    return _id_counter[0]

from datetime import date, datetime, timedelta

@app.get("/", response_class=HTMLResponse)
async def index():
    tpl = jinja_env.get_template("index.html")
    return HTMLResponse(tpl.render())

class LoginReq(BaseModel):
    phone: str

@app.post("/api/login")
async def member_login(req: LoginReq):
    phone = req.phone
    masked = phone[:3] + "****" + phone[-4:]
    if masked in members_db:
        return {"success": True, "member": members_db[masked]}
    fake = {"phone": masked, "name": phone[-4:] + "号会员", "avatar": "👤",
        "member_since": str(date.today()), "total_sessions": 0, "trainer": "待分配"}
    members_db[masked] = fake
    return {"success": True, "member": fake}

@app.post("/api/coach/login")
async def coach_login(req: LoginReq):
    phone = req.phone
    masked = phone[:3] + "****" + phone[-4:]
    for c in coach_accounts:
        if c["phone"] == masked:
            return {"success": True, "coach": c}
    return {"success": False, "error": "账号不存在"}

@app.post("/api/member/records")
async def get_member_records(req: LoginReq):
    phone = req.phone
    masked = phone[:3] + "****" + phone[-4:]
    records = members_db.get(masked, {}).get("records", [])
    return {"records": records}

class GripLog(BaseModel):
    phone: str
    value: float
    note: Optional[str] = ""

@app.post("/api/member/grip/add")
async def add_grip(req: GripLog):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    if phone not in member_grip:
        member_grip[phone] = []
    entry = {"id": next_id(), "date": str(date.today()), "value": req.value, "note": req.note}
    member_grip[phone].append(entry)
    return {"success": True}

@app.post("/api/member/grip/list")
async def list_grip(req: LoginReq):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    data = member_grip.get(phone, [])
    status = None
    if len(data) >= 3:
        recent = sorted(data, key=lambda x: x["id"])[-5:]
        baseline = max(d["value"] for d in data[:3])
        avg_recent = sum(d["value"] for d in recent) / len(recent)
        ratio = round(avg_recent / baseline * 100)
        if ratio < 80:
            status = {"level": "high", "label": "疲劳高风险", "icon": "🔴", "ratio": ratio, "color": "#ef4444"}
        elif ratio < 90:
            status = {"level": "mild", "label": "轻度疲劳", "icon": "🟡", "ratio": ratio, "color": "#eab308"}
        else:
            status = {"level": "normal", "label": "状态良好", "icon": "🟢", "ratio": ratio, "color": "#22c55e"}
    return {"entries": data, "fatigue_status": status}

@app.post("/api/member/grip/delete")
async def delete_grip(req: dict):
    phone = req["phone"][:3] + "****" + req["phone"][-4:]
    if phone in member_grip:
        member_grip[phone] = [d for d in member_grip[phone] if d["id"] != req.get("id")]
    return {"success": True}

class RpeSave(BaseModel):
    phone: str
    date: str
    rpe: int

@app.post("/api/member/rpe/save")
async def save_rpe(req: RpeSave):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    if phone not in member_rpe:
        member_rpe[phone] = {}
    member_rpe[phone][req.date] = req.rpe
    return {"success": True}

@app.post("/api/member/rpe/list")
async def list_rpe(req: LoginReq):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    return {"rpe": member_rpe.get(phone, {})}

@app.post("/api/member/fatigue/curve")
async def get_fatigue_curve(req: LoginReq):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    grips = member_grip.get(phone, [])
    rpes = member_rpe.get(phone, {})
    dates = set()
    for g in grips:
        dates.add(g["date"])
    for d in rpes:
        dates.add(d)
    sorted_dates = sorted(dates)
    curve = []
    for d in sorted_dates:
        entry = {"date": d}
        grip_data = [g for g in grips if g["date"] == d]
        if grip_data:
            entry["grip"] = grip_data[-1]
        if d in rpes:
            entry["rpe"] = rpes[d]
        curve.append(entry)
    return {"curve": curve}

@app.post("/api/member/meals/save")
async def save_meals(req: dict):
    phone = req["phone"][:3] + "****" + req["phone"][-4:]
    if phone not in member_meals:
        member_meals[phone] = []
    member_meals[phone].append({
        "id": next_id(), "date": str(date.today()),
        "meals": req.get("meals", []), "note": req.get("note", "")
    })
    return {"success": True}

@app.post("/api/member/meals/list")
async def list_meals(req: LoginReq):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    return {"meals": member_meals.get(phone, [])}

@app.post("/api/member/52track/get")
async def get_52track(req: LoginReq):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    track = member_meals.get("_52track_" + phone, {})
    return {"track": track}

@app.post("/api/member/52track/save")
async def save_52track(req: dict):
    phone = req["phone"][:3] + "****" + req["phone"][-4:]
    member_meals["_52track_" + phone] = req.get("track", {})
    return {"success": True}

@app.get("/api/nutrition/guides")
async def get_nutrition_guides():
    return {"guides": nutrition_guides}

class PhotoUpload(BaseModel):
    phone: str
    data_url: str
    label: Optional[str] = ""
    note: Optional[str] = ""

@app.post("/api/member/photos/upload")
async def upload_photo(req: PhotoUpload):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    if phone not in member_photos:
        member_photos[phone] = []
    member_photos[phone].append({
        "id": next_id(), "date": str(date.today()),
        "data_url": req.data_url, "label": req.label or "记录", "note": req.note
    })
    return {"success": True}

@app.post("/api/member/photos/list")
async def list_photos(req: LoginReq):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    return {"photos": member_photos.get(phone, [])}

@app.post("/api/member/photos/delete")
async def delete_photo(req: dict):
    phone = req["phone"][:3] + "****" + req["phone"][-4:]
    if phone in member_photos:
        member_photos[phone] = [p for p in member_photos[phone] if p["id"] != req.get("photo_id")]
    return {"success": True}

class StrengthAdd(BaseModel):
    phone: str
    squats: Optional[int] = None
    bench: Optional[int] = None
    deadlift: Optional[int] = None
    press: Optional[int] = None
    pullup: Optional[int] = None
    note: Optional[str] = ""

@app.post("/api/member/strength/add")
async def add_strength(req: StrengthAdd):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    if phone not in member_strength:
        member_strength[phone] = []
    member_strength[phone].append({
        "id": next_id(), "date": str(date.today()),
        "squats": req.squats, "bench": req.bench, "deadlift": req.deadlift,
        "press": req.press, "pullup": req.pullup, "note": req.note
    })
    return {"success": True}

@app.post("/api/member/strength/list")
async def list_strength(req: LoginReq):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    return {"entries": member_strength.get(phone, [])}

@app.post("/api/member/strength/delete")
async def delete_strength(req: dict):
    phone = req["phone"][:3] + "****" + req["phone"][-4:]
    if phone in member_strength:
        member_strength[phone] = [e for e in member_strength[phone] if e["id"] != req.get("entry_id")]
    return {"success": True}

class CoachPlanSave(BaseModel):
    phone: str
    member_phone: str
    content: str

@app.post("/api/coach/plan/save")
async def coach_save_plan(req: CoachPlanSave):
    mphone = req.member_phone
    if mphone not in coach_plans:
        coach_plans[mphone] = []
    coach_plans[mphone].append({
        "id": next_id(), "date": str(date.today()),
        "content": req.content, "status": "已发布"
    })
    return {"success": True}

class CoachRecordSave(BaseModel):
    phone: str
    member_phone: str
    type: str
    duration: str
    content: str
    summary: str

@app.post("/api/coach/record/add")
async def coach_add_record(req: CoachRecordSave):
    mphone = req.member_phone
    if mphone not in coach_extra_records:
        coach_extra_records[mphone] = []
    coach_extra_records[mphone].append({
        "id": next_id(), "date": str(date.today()),
        "type": req.type, "duration": req.duration,
        "content": req.content, "summary": req.summary,
        "mood": "📝 教练记录"
    })
    return {"success": True}

@app.post("/api/coach/member/data")
async def coach_member_data(req: dict):
    mphone = req.get("member_phone", "")
    records = members_db.get(mphone, {}).get("records", [])
    extra = coach_extra_records.get(mphone, [])
    plans = coach_plans.get(mphone, [])
    return {"records": records + extra, "plans": plans}

@app.post("/api/coach/member/grip")
async def coach_member_grip(req: dict):
    mphone = req.get("phone", "")
    data = member_grip.get(mphone, [])
    status = None
    if len(data) >= 3:
        recent = sorted(data, key=lambda x: x["id"])[-5:]
        baseline = max(d["value"] for d in data[:3])
        avg_recent = sum(d["value"] for d in recent) / len(recent)
        ratio = round(avg_recent / baseline * 100)
        if ratio < 80:
            status = {"level": "high", "label": "疲劳高风险", "icon": "🔴", "ratio": ratio, "color": "#ef4444"}
        elif ratio < 90:
            status = {"level": "mild", "label": "轻度疲劳", "icon": "🟡", "ratio": ratio, "color": "#eab308"}
        else:
            status = {"level": "normal", "label": "状态良好", "icon": "🟢", "ratio": ratio, "color": "#22c55e"}
    return {"fatigue_status": status}

@app.post("/api/coach/member/list")
async def coach_member_list(req: LoginReq):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    for c in coach_accounts:
        if c["phone"] == phone:
            return {"members": c["members"]}
    return {"members": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
