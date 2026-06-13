f=open("C:\\Users\\79018\\Documents\\体能训练资料库\\fitness_web\\static\\js\\app.js","r",encoding="utf-8")
c=f.read()
f.close()

# Replace the renderRecords function
old_render='''function renderRecords(){const e=document.getElementById("recordList");if(!R.length){e.innerHTML='<div class="record-empty">暂无训练记录 💪</div>';return}e.innerHTML=R.map(r=>{const ic=r.mood==="📝 教练记录";return `<div class="record-card"><div class="record-card-header"><div class="record-date">${r.date}</div><div class="record-meta"><span class="record-type">${r.type}</span><span class="record-duration">${r.duration}</span>${ic?'<span class="record-source-coach">教练</span>':''}</div></div><div class="record-mood">${r.mood}</div><div class="record-content">${r.content}</div>${r.summary?`<div class="record-summary"><div class="record-summary-label">📝 教练点评</div>${r.summary}</div>`:""}</div>`}).join("")}'''

new_render='''function renderRecords(){const e=document.getElementById("recordList");if(!R.length){e.innerHTML='<div class="record-empty">暂无训练记录 💪</div>';return}e.innerHTML=R.map(r=>{const ic=r.mood==="📝 教练记录";const rpeV=currentRpe[r.date];return `<div class="record-card"><div class="record-card-header"><div class="record-date">${r.date}</div><div class="record-meta"><span class="record-type">${r.type}</span><span class="record-duration">${r.duration}</span>${ic?'<span class="record-source-coach">教练</span>':''}</div></div><div class="record-mood">${r.mood}</div><div class="record-content">${r.content}</div><div class="rpe-label">训练疲劳度（RPE）</div><div class="rpe-row">${[1,2,3,4,5,6,7,8,9,10].map(n=>{let cls="rpe-btn";if(n>=8)cls+=" rpe-high";else if(n>=5)cls+=" rpe-mid";else cls+=" rpe-low";if(rpeV===n)cls+=" selected";return `<button class="${cls}" onclick="saveRpe('${r.date}',${n})">${n}</button>`}).join("")}</div>${rpeV?`<div class="rpe-saved">✓ 已评 RPE ${rpeV}</div>`:`<div class="rpe-hint"><span>轻松</span><span>适中</span><span>极限</span></div>`}</div>`}).join("")}'''

if old_render in c:
    c=c.replace(old_render,new_render)
else:
    print("renderRecords not found")

# Add currentRpe variable after R=[] initialization
old_init="let M=null,C=null,R=[],P=[],S=[],KD={};"
new_init="let M=null,C=null,R=[],P=[],S=[],KD={},currentRpe={};"
c=c.replace(old_init,new_init)

# Replace loadRecords to also load RPE
old_loadR="async function loadRecords(){const p=localStorage.getItem(\"fitness_phone\");if(!p)return;try{const d=await API.post(\"/api/member/records\",{phone:p});R=d.records||[];renderRecords()}catch(e){}}"
new_loadR="async function loadRecords(){const p=localStorage.getItem(\"fitness_phone\");if(!p)return;try{const[d,r]=await Promise.all([API.post(\"/api/member/records\",{phone:p}),API.post(\"/api/member/rpe/list\",{phone:p})]);R=d.records||[];currentRpe=r.rpe||{};renderRecords()}catch(e){}}"
c=c.replace(old_loadR,new_loadR)

# Replace loadGrip to also load curve
old_grip="async function loadGrip(){const p=localStorage.getItem(\"fitness_phone\");if(!p)return;try{const d=await API.post(\"/api/member/grip/list\",{phone:p});renderGripStatus(d.fatigue_status);renderGripList(d.grip)}catch(e){}}"
new_grip="async function loadGrip(){const p=localStorage.getItem(\"fitness_phone\");if(!p)return;try{const[g,cv]=await Promise.all([API.post(\"/api/member/grip/list\",{phone:p}),API.post(\"/api/member/fatigue/curve\",{phone:p})]);renderGripStatus(g.fatigue_status);renderGripList(g.grip);renderCurve(cv.curve||[])}catch(e){}}"
c=c.replace(old_grip,new_grip)

# Add RPE save + curve render functions before the tab switching section
old_switch="// ===== Tab切换 ====="
rpe_funcs='''
// ===== RPE 评分 =====
async function saveRpe(date,val){
    const p=localStorage.getItem("fitness_phone");if(!p)return;
    await API.post("/api/member/rpe/save",{phone:p,date:date,value:val});
    currentRpe[date]=val;
    renderRecords()
}

// ===== 疲劳曲线 =====
function renderCurve(curve){
    const el=document.getElementById("curveChart");
    if(!el)return;
    if(!curve||curve.length<2){el.innerHTML='<div class="curve-empty">记录握力和RPE后自动生成 📊</div>';return}
    let html="<table class=\\"curve-table\\"><tr><td class=\\"curve-row-label\\"></td>";
    curve.forEach(c=>{html+='<td class="date-label">'+c.date.slice(5)+"</td>"});
    html+="</tr><tr><td class=\\"curve-row-label\\">\\u270a</td>";
    curve.forEach(c=>{
        if(c.grip){
            let color="#22c55e";
            if(c.grip._fatigue==="high")color="#ef4444";
            else if(c.grip._fatigue==="mild")color="#eab308";
            html+='<td><div class="curve-grip-dot" style="background:'+color+'">'+c.grip.value.toFixed(0)+"</div></td>"
        }else html+='<td><div class="curve-grip-value">-</div></td>'
    });
    html+="</tr><tr><td class=\\"curve-row-label\\">RPE</td>";
    curve.forEach(c=>{
        if(c.rpe)html+='<td><div class="curve-rpe-dot">'+c.rpe+"</div></td>";
        else html+='<td><span class="curve-rpe-empty">-</span></td>'
    });
    html+="</tr></table>";
    el.innerHTML=html
}'''

c=c.replace(old_switch,rpe_funcs+old_switch)

f=open("C:\\Users\\79018\\Documents\\体能训练资料库\\fitness_web\\static\\js\\app.js","w",encoding="utf-8")
f.write(c)
f.close()
print("OK")
