f=open("C:\\Users\\79018\\Documents\\体能训练资料库\\fitness_web\\main.py","r",encoding="utf-8")
c=f.read()
f.close()

old1="member_grip = {}  # phone -> [{id, date, value, morning_note}]"
new1="member_grip = {}  # phone -> [{id, date, value, morning_note}]\nmember_rpe = {}   # phone -> {date: rpe_value}"
c=c.replace(old1,new1)

old2='@app.get("/api/health")'
new2='''\n# --- RPE ---
@app.post("/api/member/rpe/save")
async def save_rpe(req):
    body = await req.json()
    phone = body.get("phone"); date = body.get("date"); value = body.get("value")
    if phone and date:
        if phone not in member_rpe: member_rpe[phone] = {}
        member_rpe[phone][date] = value
    return {"success": True}

@app.post("/api/member/rpe/list")
async def get_rpe(req: LoginRequest):
    return {"rpe": member_rpe.get(req.phone, {})}

@app.post("/api/member/fatigue/curve")
async def get_fatigue_curve(req: LoginRequest):
    gd = member_grip.get(req.phone, [])
    gd.sort(key=lambda g: g["date"]+g.get("time",""), reverse=True)
    rd = member_rpe.get(req.phone, {})
    from datetime import date, timedelta
    td = date.today(); cv = []
    for i in range(13, -1, -1):
        d = str(td - timedelta(days=i))
        grip = None
        for g in gd:
            if g["date"] == d: grip = g; break
        rpe = rd.get(d)
        if grip or rpe: cv.append({"date": d, "grip": grip, "rpe": rpe})
    return {"curve": cv}

'''
c=c.replace(old2,new2)
f=open("C:\\Users\\79018\\Documents\\体能训练资料库\\fitness_web\\main.py","w",encoding="utf-8")
f.write(c)
f.close()
print("OK")
