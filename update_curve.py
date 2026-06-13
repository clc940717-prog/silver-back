f=open("C:\\Users\\79018\\Documents\\体能训练资料库\\fitness_web\\main.py","r",encoding="utf-8")
c=f.read()
f.close()

old='''    gd = member_grip.get(req.phone, [])
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
    return {"curve": cv}'''

new='''    gd = member_grip.get(req.phone, [])
    gd.sort(key=lambda g: g["date"]+g.get("time",""), reverse=True)
    rd = member_rpe.get(req.phone, {})
    from datetime import date, timedelta
    td = date.today(); cv = []
    # Calculate baseline for fatigue detection
    vals = [g["value"] for g in gd]
    for i in range(13, -1, -1):
        d = str(td - timedelta(days=i))
        grip = None; fat = None
        for g in gd:
            if g["date"] == d: grip = g; break
        if grip:
            bl_vals = [v for v in vals if v != grip["value"]]
            if bl_vals:
                bl = sum(bl_vals[:5]) / min(len(bl_vals[:5]),1)
                if bl>0:
                    r = grip["value"]/bl
                    if r >= 0.95: fat = "normal"
                    elif r >= 0.90: fat = "mild"
                    else: fat = "high"
            if fat: grip["_fatigue"] = fat
        rpe = rd.get(d)
        if grip or rpe: cv.append({"date": d, "grip": grip, "rpe": rpe})
    return {"curve": cv}'''

if old in c:
    c=c.replace(old,new)
    f=open("C:\\Users\\79018\\Documents\\体能训练资料库\\fitness_web\\main.py","w",encoding="utf-8")
    f.write(c)
    f.close()
    print("OK")
else:
    print("NOT FOUND")
