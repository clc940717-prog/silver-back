# -*- coding: utf-8 -*-
import os, sqlite3, json
from datetime import date, datetime, timedelta
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

# --- Database ---
DB_PATH = os.path.join(BASE_DIR, "silverback.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL");
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.executescript("""
CREATE TABLE IF NOT EXISTS coaches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone TEXT UNIQUE, name TEXT, avatar TEXT, badge TEXT,
    password TEXT DEFAULT "");

CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone TEXT UNIQUE, name TEXT, avatar TEXT,
    member_since TEXT, total_sessions INTEGER DEFAULT 0,
    trainer TEXT, trainer_phone TEXT, password TEXT DEFAULT "");

CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_phone TEXT, date TEXT, type TEXT, duration TEXT,
    content TEXT, mood TEXT, summary TEXT DEFAULT "",
    source TEXT DEFAULT "member");

CREATE TABLE IF NOT EXISTS rpe (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_phone TEXT, date TEXT UNIQUE, rpe INTEGER);

CREATE TABLE IF NOT EXISTS grips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_phone TEXT, date TEXT, value REAL, note TEXT DEFAULT "");

CREATE TABLE IF NOT EXISTS meals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_phone TEXT, date TEXT, meals TEXT, note TEXT DEFAULT "");

CREATE TABLE IF NOT EXISTS fast52 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_phone TEXT, day_key TEXT, status TEXT DEFAULT "normal",
    UNIQUE(member_phone, day_key));

CREATE TABLE IF NOT EXISTS photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_phone TEXT, date TEXT, data_url TEXT,
    label TEXT DEFAULT "", note TEXT DEFAULT "");

CREATE TABLE IF NOT EXISTS strength (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_phone TEXT, date TEXT,
    squats INTEGER, bench INTEGER, deadlift INTEGER,
    press INTEGER, pullup INTEGER, note TEXT DEFAULT "");

CREATE TABLE IF NOT EXISTS profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_phone TEXT UNIQUE,
    name TEXT DEFAULT "",
    age INTEGER,
    weight REAL,
    muscle REAL,
    fat REAL,
    body_fat REAL);

CREATE TABLE IF NOT EXISTS plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_phone TEXT, date TEXT, content TEXT, status TEXT DEFAULT "");

    """ )
    conn.commit()
    conn.close()

init_db()

# --- Seed data ---
COACHES_DATA = [{"id": 1, "name": "clc", "avatar": "🏋️", "badge": "Silver Back", "phone": "152****1563"}]
TRANSFORMATIONS = [{"id": 1, "name": "小雅", "avatar": "👩", "period": "3个月", "from_data": "体脂 32%", "to_data": "体脂 24%", "weight_change": "−12斤", "story": "从来不爱运动的办公室白领，从第一次卧推空杆都发抖，到能完成标准引体向上。她说最大的收获不是瘦了，是爱上了流汗的感觉。", "tags": ["减脂", "塑形"], "highlight": "体脂下降8% · 引体向上突破"}, {"id": 2, "name": "阿杰", "avatar": "👨", "period": "6个月", "from_data": "深蹲 40kg", "to_data": "深蹲 120kg", "weight_change": "＋10kg肌", "story": "健身3年一直原地踏步，瓶颈期困扰了他整整一年。经过系统周期化训练和动作模式重建，半年实现成绩翻倍。", "tags": ["增肌", "力量"], "highlight": "深蹲 40→120kg · 三大项突破300kg"}, {"id": 3, "name": "蕾蕾", "avatar": "👩‍💼", "period": "4个月", "from_data": "腹直肌分离2指", "to_data": "完全恢复", "weight_change": "−8斤", "story": "产后6个月来到工作室。从不敢做任何核心动作，到可以完成平板支撑2分钟，腹直肌分离完全闭合。", "tags": ["产后恢复", "康复"], "highlight": "腹直肌闭合 · 核心力量重建"}, {"id": 4, "name": "老陈", "avatar": "👨‍🦰", "period": "8个月", "from_data": "体脂 28%", "to_data": "体脂 18%", "weight_change": "−16斤", "story": "45岁的中年企业家，体检报告亮红灯后下定决心。从最开始走15分钟都喘，到现在每周5练，体检指标全部恢复正常。", "tags": ["减脂", "健康管理"], "highlight": "脂肪肝逆转 · 体检指标全正常"}]
PRICING = [{"id": 1, "name": "单次体验", "sessions": 1, "price": 399, "unit_price": 399, "tag": "体验", "features": ["1对1 专业指导", "体态评估", "训练计划制定"], "popular": False}, {"id": 2, "name": "10节私教", "sessions": 10, "price": 3599, "unit_price": 360, "tag": "入门", "features": ["1对1 专业指导", "体态评估", "训练计划制定", "饮食建议", "课后小结推送"], "popular": False}, {"id": 3, "name": "20节私教", "sessions": 20, "price": 6399, "unit_price": 320, "tag": "推荐", "features": ["1对1 专业指导", "体态评估", "训练计划制定", "饮食建议", "课后小结推送", "月度体测", "灵活约课"], "popular": True}, {"id": 4, "name": "40节私教", "sessions": 40, "price": 11199, "unit_price": 280, "tag": "超值", "features": ["1对1 专业指导", "体态评估", "训练计划制定", "饮食建议", "课后小结推送", "月度体测", "灵活约课", "无限次自主训练"], "popular": False}]
NUTRITION_GUIDES = [{"id": 1, "title": "什么是5:2轻断食？", "content": "5:2轻断食是一种间歇性断食法。每周5天正常饮食，选择不连续2天进行低热量摄入（女性约500kcal，男性约600kcal）。研究表明5:2断食法对减脂、胰岝素敏感度提升和细胞自噬有显著效果。"}, {"id": 2, "title": "断食日怎么吃？", "content": "断食日建议摄入高蛋白、高纤维的食物，如鸡胸肉、鱼虾、绿叶蔬菜、蛋类。避免精制碳水和含糖饮料。可以将热量分配到1-2餐中，根据个人习惯选择早餐+晚餐或仅午餐。"}, {"id": 3, "title": "非断食日注意事项", "content": "非断食日不需要严格限制，但建议保持均衡营养。蛋白质摄入建议达到体重kg×1.2-1.6g，保证训练后营养补充。不建议在非断食日暴饮暴食。"}, {"id": 4, "title": "训练日与断食的搭配", "content": "高强度训练日尽量安排在非断食日。若断食日有训练，建议训练前摄入少量快碳（如一根香蕉），训练后立即补充蛋白质。断食日适合进行低强度有氧或恢复性训练。"}, {"id": 5, "title": "适合哪些人群？", "content": "5:2轻断食适合体重正常至超重的健康人群，尤其适合：减脂平台期、工作忙碌难以每日控制饮食者、想要改善代谢健康的人群。不建议孕妇、青少年、糖尿病患者、饮食失调史者使用。"}, {"id": 6, "title": "常见问题", "content": "Q:断食日会很饿吗？\nA:通常2-3周后身体会适应，饥饿感明显下降。\n\nQ:可以喝咖啡和茶吗？\nA:可以，建议不加糖奶。黑咖啡和茶有助于抑制饥饿。\n\nQ:多久能看到效果？\nA:坚持4-6周可以看到明显体脂变化，配合训练效果更佳。"}]

def seed_if_empty():
    conn = get_db()
    c = conn.cursor()
    # Always reseed
    for co in COACHES_DATA:
            c.execute("INSERT OR REPLACE INTO coaches(phone,name,avatar,badge) VALUES (?,?,?,?)",
                (co["phone"], co["name"], co["avatar"], co["badge"]))
    conn.commit()
    conn.close()

seed_if_empty()

# --- Home ---
@app.get("/", response_class=HTMLResponse)
async def index():
    tpl = jinja_env.get_template("index.html")
    return HTMLResponse(tpl.render())

class LoginReq(BaseModel):
    phone: str
    password: Optional[str] = ""

# --- Member Login ---
@app.post("/api/login")
async def member_login(req: LoginReq):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    conn = get_db()
    row = conn.execute("SELECT * FROM members WHERE phone=?", (phone,)).fetchone()
    if row:
        return {"success": True, "member": dict(row)}
    # Auto-register
    name = phone[-4:] + "号会员"
    conn.execute("INSERT INTO members(phone,name,avatar,member_since,total_sessions,trainer,trainer_phone) VALUES (?,?,?,?,?,?,?)",
        (phone, name, "👤", str(date.today()), 0, "clc", "152****1563"))
    conn.commit()
    row = conn.execute("SELECT * FROM members WHERE phone=?", (phone,)).fetchone()
    conn.close()
    return {"success": True, "member": dict(row)}

# --- Coach Login ---
@app.post("/api/coach/login")
async def coach_login(req: LoginReq):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    conn = get_db()
    row = conn.execute("SELECT * FROM coaches WHERE phone=?", (phone,)).fetchone()
    if not row:
        conn.close()
        return {"success": False, "error": "账号不存在"}
    coach = dict(row)
    # Get coach members
    members = conn.execute("SELECT phone,name,avatar,member_since,total_sessions FROM members WHERE trainer_phone=? OR trainer=?",
        (phone, coach["name"])).fetchall()
    coach["members"] = [dict(m) for m in members]
    conn.close()
    return {"success": True, "coach": coach}

# --- Member Records ---
@app.post("/api/member/records")
async def get_member_records(req: LoginReq):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    conn = get_db()
    rows = conn.execute("SELECT * FROM records WHERE member_phone=? ORDER BY date DESC", (phone,)).fetchall()
    conn.close()
    return {"records": [dict(r) for r in rows]}

class GripLog(BaseModel):
    phone: str
    value: float
    note: Optional[str] = ""

@app.post("/api/member/grip/add")
async def add_grip(req: GripLog):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    conn = get_db()
    conn.execute("INSERT INTO grips(member_phone,date,value,note) VALUES (?,?,?,?)",
        (phone, str(date.today()), req.value, req.note))
    conn.commit()
    conn.close()
    return {"success": True}

@app.post("/api/member/grip/list")
async def list_grip(req: LoginReq):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    conn = get_db()
    rows = conn.execute("SELECT * FROM grips WHERE member_phone=? ORDER BY id", (phone,)).fetchall()
    data = [dict(r) for r in rows]
    status = None
    if len(data) >= 3:
        recent = data[-5:]
        baseline = max(d["value"] for d in data[:3])
        avg_recent = sum(d["value"] for d in recent) / len(recent)
        ratio = round(avg_recent / baseline * 100)
        if ratio < 80:
            status = {"level": "high", "label": "疲劳高风险", "icon": "🔴", "ratio": ratio, "color": "#ef4444"}
        elif ratio < 90:
            status = {"level": "mild", "label": "轻度疲劳", "icon": "🟡", "ratio": ratio, "color": "#eab308"}
        else:
            status = {"level": "normal", "label": "状态良好", "icon": "🟢", "ratio": ratio, "color": "#22c55e"}
    conn.close()
    return {"entries": data, "fatigue_status": status}

@app.post("/api/member/grip/delete")
async def delete_grip(req: dict):
    phone = req["phone"][:3] + "****" + req["phone"][-4:]
    conn = get_db()
    conn.execute("DELETE FROM grips WHERE member_phone=? AND id=?", (phone, req.get("id")))
    conn.commit()
    conn.close()
    return {"success": True}

class RpeSave(BaseModel):
    phone: str
    date: str
    rpe: int

@app.post("/api/member/rpe/save")
async def save_rpe(req: RpeSave):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    conn = get_db()
    conn.execute("INSERT OR REPLACE INTO rpe(member_phone,date,rpe) VALUES (?,?,?)",
        (phone, req.date, req.rpe))
    conn.commit()
    conn.close()
    return {"success": True}

@app.post("/api/member/rpe/list")
async def list_rpe(req: LoginReq):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    conn = get_db()
    rows = conn.execute("SELECT date,rpe FROM rpe WHERE member_phone=?", (phone,)).fetchall()
    conn.close()
    return {"rpe": {r["date"]: r["rpe"] for r in rows}}

@app.post("/api/member/fatigue/curve")
async def get_fatigue_curve(req: LoginReq):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    conn = get_db()
    grips = conn.execute("SELECT * FROM grips WHERE member_phone=? ORDER BY id", (phone,)).fetchall()
    rpes = conn.execute("SELECT date,rpe FROM rpe WHERE member_phone=?", (phone,)).fetchall()
    conn.close()
    rpe_dict = {r["date"]: r["rpe"] for r in rpes}
    dates = set()
    for g in grips:
        dates.add(g["date"])
    for d in rpe_dict:
        dates.add(d)
    curve = []
    for d in sorted(dates):
        entry = {"date": d}
        gd = [dict(g) for g in grips if g["date"] == d]
        if gd: entry["grip"] = gd[-1]
        if d in rpe_dict: entry["rpe"] = rpe_dict[d]
        curve.append(entry)
    return {"curve": curve}

@app.post("/api/member/meals/save")
async def save_meals(req: dict):
    phone = req["phone"][:3] + "****" + req["phone"][-4:]
    conn = get_db()
    conn.execute("INSERT INTO meals(member_phone,date,meals,note) VALUES (?,?,?,?)",
        (phone, str(date.today()), json.dumps(req.get("meals",[])), req.get("note","")))
    conn.commit()
    conn.close()
    return {"success": True}

@app.post("/api/member/meals/list")
async def list_meals(req: LoginReq):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    conn = get_db()
    rows = conn.execute("SELECT * FROM meals WHERE member_phone=? ORDER BY id", (phone,)).fetchall()
    conn.close()
    meals = []
    for r in rows:
        d = dict(r)
        try: d["meals"] = json.loads(d["meals"])
        except: pass
        meals.append(d)
    return {"meals": meals}

@app.post("/api/member/52track/get")
async def get_52track(req: LoginReq):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    conn = get_db()
    rows = conn.execute("SELECT day_key,status FROM fast52 WHERE member_phone=?", (phone,)).fetchall()
    conn.close()
    return {"track": {r["day_key"]: r["status"] for r in rows}}

@app.post("/api/member/52track/save")
async def save_52track(req: dict):
    phone = req["phone"][:3] + "****" + req["phone"][-4:]
    track = req.get("track", {})
    conn = get_db()
    for day_key, status in track.items():
        conn.execute("INSERT OR REPLACE INTO fast52(member_phone,day_key,status) VALUES (?,?,?)",
            (phone, day_key, status))
    conn.commit()
    conn.close()
    return {"success": True}

@app.get("/api/nutrition/guides")
async def get_nutrition_guides():
    return {"guides": NUTRITION_GUIDES}

class PhotoUpload(BaseModel):
    phone: str
    data_url: str
    label: Optional[str] = ""
    note: Optional[str] = ""

@app.post("/api/member/photos/upload")
async def upload_photo(req: PhotoUpload):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    conn = get_db()
    conn.execute("INSERT INTO photos(member_phone,date,data_url,label,note) VALUES (?,?,?,?,?)",
        (phone, str(date.today()), req.data_url, req.label or "记录", req.note))
    conn.commit()
    conn.close()
    return {"success": True}

@app.post("/api/member/photos/list")
async def list_photos(req: LoginReq):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    conn = get_db()
    rows = conn.execute("SELECT * FROM photos WHERE member_phone=? ORDER BY id", (phone,)).fetchall()
    conn.close()
    return {"photos": [dict(r) for r in rows]}

@app.post("/api/member/photos/delete")
async def delete_photo(req: dict):
    phone = req["phone"][:3] + "****" + req["phone"][-4:]
    conn = get_db()
    conn.execute("DELETE FROM photos WHERE member_phone=? AND id=?", (phone, req.get("photo_id")))
    conn.commit()
    conn.close()
    return {"success": True}

class ProfileInfo(BaseModel):
    phone: str
    name: Optional[str] = ""
    age: Optional[int] = None
    weight: Optional[float] = None
    muscle: Optional[float] = None
    fat: Optional[float] = None
    body_fat: Optional[float] = None

@app.post("/api/member/profile/save")
async def save_profile(req: ProfileInfo):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    conn = get_db()
    conn.execute("INSERT OR REPLACE INTO profile(member_phone,name,age,weight,muscle,fat,body_fat) VALUES (?,?,?,?,?,?,?)",
        (phone, req.name, req.age, req.weight, req.muscle, req.fat, req.body_fat))
    conn.commit()
    conn.close()
    return {"success": True}

@app.post("/api/member/profile/get")
async def get_profile(req: LoginReq):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    conn = get_db()
    row = conn.execute("SELECT * FROM profile WHERE member_phone=?", (phone,)).fetchone()
    conn.close()
    return {"profile": dict(row) if row else None}



class CoachPlanSave(BaseModel):
    phone: str
    member_phone: str
    content: str

@app.post("/api/coach/plan/save")
async def coach_save_plan(req: CoachPlanSave):
    conn = get_db()
    conn.execute("INSERT INTO plans(member_phone,date,content,status) VALUES (?,?,?,?)",
        (req.member_phone, str(date.today()), req.content, "已发布"))
    conn.commit()
    conn.close()
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
    conn = get_db()
    conn.execute("INSERT INTO records(member_phone,date,type,duration,content,mood,summary,source) VALUES (?,?,?,?,?,?,?,?)",
        (req.member_phone, str(date.today()), req.type, req.duration, req.content, "📝 教练记录", req.summary, "coach"))
    conn.commit()
    conn.close()
    return {"success": True}

@app.post("/api/coach/member/data")
async def coach_member_data(req: dict):
    mphone = req.get("member_phone", "")
    conn = get_db()
    records = conn.execute("SELECT * FROM records WHERE member_phone=? ORDER BY date DESC", (mphone,)).fetchall()
    plans = conn.execute("SELECT * FROM plans WHERE member_phone=? ORDER BY date DESC", (mphone,)).fetchall()
    conn.close()
    return {"records": [dict(r) for r in records], "plans": [dict(p) for p in plans]}

@app.post("/api/coach/member/grip")
async def coach_member_grip(req: dict):
    mphone = req.get("phone", "")
    conn = get_db()
    rows = conn.execute("SELECT * FROM grips WHERE member_phone=? ORDER BY id", (mphone,)).fetchall()
    data = [dict(r) for r in rows]
    status = None
    if len(data) >= 3:
        recent = data[-5:]
        baseline = max(d["value"] for d in data[:3])
        avg_recent = sum(d["value"] for d in recent) / len(recent)
        ratio = round(avg_recent / baseline * 100)
        if ratio < 80:
            status = {"level": "high", "label": "疲劳高风险", "icon": "🔴", "ratio": ratio, "color": "#ef4444"}
        elif ratio < 90:
            status = {"level": "mild", "label": "轻度疲劳", "icon": "🟡", "ratio": ratio, "color": "#eab308"}
        else:
            status = {"level": "normal", "label": "状态良好", "icon": "🟢", "ratio": ratio, "color": "#22c55e"}
    conn.close()
    return {"fatigue_status": status}

@app.post("/api/coach/member/list")
async def coach_member_list(req: LoginReq):
    phone = req.phone[:3] + "****" + req.phone[-4:]
    conn = get_db()
    coach = conn.execute("SELECT * FROM coaches WHERE phone=?", (phone,)).fetchone()
    if not coach:
        conn.close()
        return {"members": []}
    members = conn.execute("SELECT phone,name,avatar,member_since,total_sessions FROM members WHERE trainer_phone=? OR trainer=?",
        (phone, coach["name"])).fetchall()
    conn.close()
    return {"members": [dict(m) for m in members]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
