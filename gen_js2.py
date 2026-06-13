import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

js = """const API={async get(u){const r=await fetch(u);return r.json()},async post(u,b){const r=await fetch(u,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(b)});return r.json()}};

let M=null,C=null,R=[],P=[],S=[],KD={},currentRpe={};

function showPage(id){document.querySelectorAll(".page").forEach(p=>p.classList.remove("active"));document.getElementById(id).classList.add("active");window.scrollTo(0,0)}

function updateNav(){
  const n=document.getElementById("topNav"),u=document.getElementById("navUser"),c=document.getElementById("navCoachUser");
  if(!C&&!M){n.style.display="none";return}
  n.style.display="flex";
  if(C){u.style.display="none";c.style.display="flex";document.getElementById("navCoachAvatar").textContent=C.avatar;document.getElementById("navCoachName").textContent=C.name;return}
  c.style.display="none";u.style.display="flex";document.getElementById("navUserAvatar").textContent=M.avatar;document.getElementById("navUserName").textContent=M.name
}

function switchLoginTab(t){
  document.querySelectorAll(".login-page-tab").forEach(b=>b.classList.remove("active"));
  document.querySelectorAll(".login-page-form").forEach(f=>f.classList.remove("active"));
  if(t==="member"){document.getElementById("tabMemberBtn").classList.add("active");document.getElementById("formMember").classList.add("active")}
  else{document.getElementById("tabCoachBtn").classList.add("active");document.getElementById("formCoach").classList.add("active")}
}

async function handleLogin(){
  const p=document.getElementById("loginPhone").value.trim();
  if(p.length<11){document.getElementById("loginPhone").style.borderColor="#ff4444";return}
  document.getElementById("loginPhone").style.borderColor="";
  try{
    const d=await API.post("/api/login",{phone:p});
    if(d.success){
      M=d.member;C=null;
      localStorage.setItem("fitness_member",JSON.stringify(d.member));
      localStorage.setItem("fitness_phone",p);
      localStorage.removeItem("fitness_coach");
      updateNav();renderMember();showPage("page-member")
    }
  }catch(e){alert("登录失败")}
}

async function handleCoachLogin(){
  const p=document.getElementById("coachLoginPhone").value.trim();
  if(p.length<11){document.getElementById("coachLoginPhone").style.borderColor="#ff4444";return}
  document.getElementById("coachLoginPhone").style.borderColor="";
  try{
    const d=await API.post("/api/coach/login",{phone:p});
    if(d.success){
      C=d.coach;M=null;
      localStorage.setItem("fitness_coach",JSON.stringify(d.coach));
      localStorage.removeItem("fitness_member");localStorage.removeItem("fitness_phone");
      updateNav();renderCoachDash();showPage("page-coach-dash")
    }else alert("账号不存在")
  }catch(e){alert("登录失败")}
}

function logout(){M=null;C=null;localStorage.removeItem("fitness_member");localStorage.removeItem("fitness_phone");localStorage.removeItem("fitness_coach");updateNav();showPage("page-login")}

function renderCoachDash(){
  if(!C)return;const c=C;
  document.getElementById("coachDashAvatar").textContent=c.avatar;
  document.getElementById("coachDashName").textContent=c.name;
  document.getElementById("coachDashBadge").textContent=c.badge;
  const el=document.getElementById("coachMemberList");
  if(!c.members.length){el.innerHTML="<div class=\\"record-empty\\">暂无学员</div>";return}
  el.innerHTML=c.members.map(m=>'<div class="coach-member-card" onclick="openCoachMemberModal(\\''+m.phone+'\\')"><div class="coach-member-avatar">'+m.avatar+'</div><div class="coach-member-info"><div class="coach-member-name">'+m.name+'</div><div class="coach-member-meta">入会 '+m.member_since+'  '+m.total_sessions+'次课</div></div><div class="coach-member-arrow">\\u203a</div></div>').join("")
}

let SMP=null;

async function openCoachMemberModal(mp){
  SMP=mp;
  document.getElementById("coachMemberModal").classList.add("active");
  document.body.style.overflow="hidden";
  const m=C.members.find(x=>x.phone===mp);
  const el=document.getElementById("coachMemberDetail");
  el.innerHTML='<div class="coach-detail-sheet-header"><div class="coach-detail-sheet-avatar">'+(m?m.avatar:"")+'</div><div><div class="coach-detail-sheet-name">'+(m?m.name:"学员")+'</div><div class="coach-detail-sheet-meta">'+(m?m.member_since+"  "+m.total_sessions+"次课":"")+'</div></div></div><div class="coach-write-section"><div class="coach-write-title">写训练计划</div><textarea class="coach-write-textarea" id="coachPlanInput" rows="3" placeholder="写下训练计划..."></textarea><button class="coach-write-btn coach-write-btn-plan" onclick="saveCoachPlan()" style="margin-top:8px">保存训练计划</button></div><div class="coach-write-section"><div class="coach-write-title">写课后小结</div><div class="coach-write-input-row"><input type="text" id="coachRecordType" placeholder="类型" value="私教课"><input type="text" id="coachRecordDuration" placeholder="时长" value="60min"></div><textarea class="coach-write-textarea" id="coachRecordContent" rows="2" placeholder="训练内容..."></textarea><textarea class="coach-write-textarea" id="coachRecordSummary" rows="2" placeholder="教练点评..." style="margin-top:8px;min-height:60px"></textarea><button class="coach-write-btn coach-write-btn-record" onclick="saveCoachRecord()">保存课后小结</button></div><div class="coach-history-title">疲劳状态（加载中...）</div><div id="coachGripStatus"></div><div class="coach-history-title">历史记录（加载中...）</div><div id="coachMemberHistory"></div>';
  await loadCoachMemberData(mp);loadCoachGripData(mp)
}

function closeCoachMemberModal(){document.getElementById("coachMemberModal").classList.remove("active");document.body.style.overflow="";SMP=null}
document.getElementById("coachMemberModal")&&document.getElementById("coachMemberModal").addEventListener("click",function(e){if(e.target===e.currentTarget)closeCoachMemberModal()});

async function loadCoachMemberData(mp){try{const d=await API.post("/api/coach/member/records",{phone:mp});KD[mp]=d;renderCoachMemberHistory(mp)}catch(e){}}

function renderCoachMemberHistory(mp){
  const d=KD[mp],el=document.getElementById("coachMemberHistory");
  if(!d||(!d.records.length&&!d.plans.length)){el.innerHTML='<div class="record-empty">暂无记录</div>';return}
  let h="";
  if(d.plans&&d.plans.length){
    h+='<div style="font-size:12px;color:#4b88ff;margin:8px 0 6px">训练计划</div>';
    [...d.plans].reverse().forEach(function(p){h+='<div class="coach-history-plan"><div class="date">'+p.date+"  "+p.status+'</div><div class="content">'+p.content+'</div></div>'})
  }
  if(d.records&&d.records.length){
    h+='<div style="font-size:12px;color:#ff6b35;margin:12px 0 6px">训练记录</div>';
    d.records.slice(0,10).forEach(function(r){
      var ic=r.mood==="教练记录";
      h+='<div class="record-card"><div class="record-card-header"><div class="record-date">'+r.date+'</div><div class="record-meta"><span class="record-type">'+r.type+'</span><span class="record-duration">'+r.duration+'</span>'+(ic?'<span class="record-source-coach">教练</span>':'')+'</div></div><div class="record-mood">'+r.mood+'</div>'+(r.content?'<div class="record-content">'+r.content+'</div>':'')+(r.summary?'<div class="record-summary"><div class="record-summary-label">教练点评</div>'+r.summary+'</div>':'')+'</div>'
    })
  }
  el.innerHTML=h
}

async function loadCoachGripData(mp){
  try{
    var d=await API.post("/api/coach/member/grip",{phone:mp});
    var el=document.getElementById("coachGripStatus");
    if(d.fatigue_status){
      var s=d.fatigue_status;
      el.innerHTML='<div style="background:rgba(255,255,255,0.02);border-radius:14px;padding:16px;text-align:center;margin-bottom:16px"><div style="font-size:36px;margin-bottom:4px">'+s.icon+'</div><div style="font-size:18px;font-weight:700;color:'+s.color+'">'+s.label+'</div><div style="font-size:13px;color:rgba(255,255,255,0.3)">当前握力为基线的 '+s.ratio+'%</div></div>'
    }else el.innerHTML='<div class="record-empty" style="padding:20px">暂无疲劳数据</div>'
  }catch(e){}
}

async function saveCoachPlan(){var c=document.getElementById("coachPlanInput").value.trim();if(!c||!SMP||!C)return;await API.post("/api/coach/plan/save",{phone:C.phone,member_phone:SMP,content:c});document.getElementById("coachPlanInput").value="";await loadCoachMemberData(SMP)}
async function saveCoachRecord(){if(!SMP||!C)return;var t=document.getElementById("coachRecordType").value.trim()||"私教课",d=document.getElementById("coachRecordDuration").value.trim()||"60min",c=document.getElementById("coachRecordContent").value.trim(),s=document.getElementById("coachRecordSummary").value.trim();if(!c&&!s){alert("请填写内容");return}await API.post("/api/coach/record/add",{phone:C.phone,member_phone:SMP,type:t,duration:d,content:c,summary:s});document.getElementById("coachRecordContent").value="";document.getElementById("coachRecordSummary").value="";await loadCoachMemberData(SMP)}

function renderMember(){
  if(!M)return;var m=M;
  document.getElementById("memberAvatar").textContent=m.avatar;
  document.getElementById("memberName").textContent=m.name;
  document.getElementById("memberSince").textContent=m.member_since;
  document.getElementById("memberTrainer").textContent=m.trainer;
  document.getElementById("memberSessions").textContent=m.total_sessions;
  switchTab("records");loadRecords();loadPhotos();loadStrength();loadGrip();loadNutrition()
}

async function loadRecords(){var p=localStorage.getItem("fitness_phone");if(!p)return;try{var a=await Promise.all([API.post("/api/member/records",{phone:p}),API.post("/api/member/rpe/list",{phone:p})]);R=a[0].records||[];currentRpe=a[1].rpe||{};renderRecords()}catch(e){}}

function renderRecords(){
  var el=document.getElementById("recordList");
  if(!R.length){el.innerHTML='<div class="record-empty">暂无训练记录</div>';return}
  el.innerHTML=R.map(function(r){
    var ic=r.mood==="教练记录",rp=currentRpe[r.date]||0;
    var bts=[1,2,3,4,5,6,7,8,9,10].map(function(n){var c="rpe-btn";if(n>=8)c+=" rpe-high";else if(n>=5)c+=" rpe-mid";else c+=" rpe-low";if(rp===n)c+=" selected";return '<button class="'+c+'" onclick="saveRpe(\\''+r.date+"',"+n+')">'+n+"</button>"}).join("");
    return '<div class="record-card"><div class="record-card-header"><div class="record-date">'+r.date+'</div><div class="record-meta"><span class="record-type">'+r.type+'</span><span class="record-duration">'+r.duration+'</span>'+(ic?'<span class="record-source-coach">教练</span>':'')+'</div></div><div class="record-mood">'+r.mood+'</div><div class="record-content">'+r.content+'</div><div class="rpe-label">训练疲劳度（RPE）</div><div class="rpe-row">'+bts+'</div>'+(rp?'<div class="rpe-saved">已评 RPE '+rp+'</div>':'<div class="rpe-hint"><span>轻松</span><span>适中</span><span>极限</span></div>')+'</div>'
  }).join("")
}

async function saveRpe(date,val){var p=localStorage.getItem("fitness_phone");if(!p)return;await API.post("/api/member/rpe/save",{phone:p,date:date,value:val});currentRpe[date]=val;renderRecords()}

async function handleGripSubmit(){var p=localStorage.getItem("fitness_phone");if(!p)return;var v=parseFloat(document.getElementById("gripInput").value);if(!v||v<=0){document.getElementById("gripInput").style.borderColor="#ff4444";return}document.getElementById("gripInput").style.borderColor="";var n=document.getElementById("gripNote").value.trim();await API.post("/api/member/grip/add",{phone:p,value:v,morning_note:n});document.getElementById("gripInput").value="";document.getElementById("gripNote").value="";await loadGrip()}

async function loadGrip(){var p=localStorage.getItem("fitness_phone");if(!p)return;try{var a=await Promise.all([API.post("/api/member/grip/list",{phone:p}),API.post("/api/member/fatigue/curve",{phone:p})]);renderGripStatus(a[0].fatigue_status);renderGripList(a[0].grip);renderCurve(a[1].curve||[])}catch(e){}}

function renderGripStatus(s){var el=document.getElementById("gripStatusContainer");if(!s){el.innerHTML="";return}el.innerHTML='<div class="grip-status-card"><div class="grip-status-icon">'+s.icon+'</div><div class="grip-status-label" style="color:'+s.color+'">'+s.label+'</div><div class="grip-status-detail">当前握力 '+s.ratio+'%  基线 '+s.baseline+'kg</div><div class="grip-status-bar"><div class="grip-status-bar-fill" style="width:'+Math.min(s.ratio,100)+'%;background:'+s.color+'"></div></div></div>'}

function renderGripList(data){var el=document.getElementById("gripList");if(!data||!data.length){el.innerHTML='<div class="record-empty">还没有记录，每天早上测一次吧</div>';return}el.innerHTML=data.slice(0,20).map(function(g){return '<div class="grip-history-card"><div class="grip-history-left"><div><div class="grip-history-value">'+g.value+'<span class="unit"> kg</span></div></div><div><div class="grip-history-meta">'+g.date+" "+g.time+'</div>'+(g.morning_note?'<div class="grip-history-note">'+g.morning_note+'</div>':'')+'</div></div><button class="grip-history-del" onclick="deleteGrip('+g.id+')">删除</button></div>'}).join("")}
async function deleteGrip(id){var p=localStorage.getItem("fitness_phone");if(!p||!confirm("确定删除？"))return;await API.post("/api/member/grip/delete",{phone:p,id});await loadGrip()}

function renderCurve(curve){var el=document.getElementById("curveChart");if(!el)return;if(!curve||curve.length<2){el.innerHTML='<div class="curve-empty">记录握力和RPE后自动生成</div>';return}var h='<table class="curve-table"><tr><td class="curve-row-label"></td>';curve.forEach(function(c){h+='<td class="date-label">'+c.date.slice(5)+"</td>"});h+='</tr><tr><td class="curve-row-label">手</td>';curve.forEach(function(c){if(c.grip){var cl="#22c55e";if(c.grip._fatigue==="high")cl="#ef4444";else if(c.grip._fatigue==="mild")cl="#eab308";h+='<td><div class="curve-grip-dot" style="background:'+cl+'">'+Math.round(c.grip.value)+"</div></td>"}else h+='<td><div class="curve-grip-value">-</div></td>'});h+='</tr><tr><td class="curve-row-label">RPE</td>';curve.forEach(function(c){if(c.rpe)h+='<td><div class="curve-rpe-dot">'+c.rpe+"</div></td>";else h+='<td><span class="curve-rpe-empty">-</span></td>"});h+="</tr></table>";el.innerHTML=h}

async function loadNutrition(){loadNutritionGuides();loadMeals();load52Track()}
var DAYS_CN=["一","二","三","四","五","六","日"],DAYS_EN=["monday","tuesday","wednesday","thursday","friday","saturday","sunday"];
async function load52Track(){var p=localStorage.getItem("fitness_phone");if(!p)return;try{var d=await API.post("/api/member/52track/get",{phone:p});render52Tracker(d.track||{})}catch(e){}}
var current52Track={};
function render52Tracker(track){current52Track=track;var w=document.getElementById("f52Week"),n=document.getElementById("f52Note");if(!w)return;var t=new Date().getDay(),ti=t===0?6:t-1;w.innerHTML=DAYS_EN.map(function(d,i){var s=track[d]||"normal",it=i===ti;return '<div class="f52-day '+s+(it?" today":"")+'" onclick="toggle52Day(\\''+d+"')\"><span class=\\"day-label\\">"+(it?"今天":"周"+DAYS_CN[i])+'</span><span class="day-icon">'+(s==="fast"?"断":"正")+"</span></div>"}).join("");var fd=DAYS_EN.filter(function(d){return track[d]==="fast"}).length;if(fd===0)n.textContent="点击选择你的断食日（推荐选2天）";else if(fd===2)n.textContent="本周 "+DAYS_EN.map(function(d,i){return track[d]==="fast"?"周"+DAYS_CN[i]:""}).filter(Boolean).join("、")+" 断食";else n.textContent="已选 "+fd+" 天，建议选2天"}
async function toggle52Day(d){var p=localStorage.getItem("fitness_phone");if(!p)return;current52Track[d]=current52Track[d]==="fast"?"normal":"fast";render52Tracker(current52Track);await API.post("/api/member/52track/save",{phone:p,track:current52Track})}
function scrollToGuide(id){var el=document.getElementById("guideContent"+id);if(el){var card=el.closest(".nutrition-guide-card");if(card)card.classList.add("open");el.scrollIntoView({behavior:"smooth",block:"center"})}else{loadNutritionGuides();setTimeout(function(){var e2=document.getElementById("guideContent"+id);if(e2){e2.closest(".nutrition-guide-card")?.classList.add("open");e2.scrollIntoView({behavior:"smooth",block:"center"})}},300)}}
async function loadNutritionGuides(){var e=document.getElementById("nutritionGuideList");if(!e)return;try{var d=await API.get("/api/nutrition/guides");e.innerHTML=d.guides.map(function(g){return '<div class="nutrition-guide-card" onclick="toggleGuide('+g.id+')"><div class="nutrition-guide-header"><span class="nutrition-guide-icon">'+g.icon+'</span><span class="nutrition-guide-info"><span class="nutrition-guide-title">'+g.title+'</span><span class="nutrition-guide-summary">'+g.summary+'</span></span><span class="nutrition-guide-arrow">></span></div><div class="nutrition-guide-content" id="guideContent'+g.id+'">'+g.content+'</div></div>'}).join("")}catch(e){}}
function toggleGuide(id){var card=document.getElementById("guideContent"+id).closest(".nutrition-guide-card");if(card)card.classList.toggle("open")}
async function handleMealSave(){var p=localStorage.getItem("fitness_phone");if(!p)return;var el=document.getElementById("mealInput"),m=(el.innerText||el.textContent||"").trim();if(!m){alert("请记录饮食内容");return}var lines=m.split("\\n").filter(function(l){return l.trim()});var meals=lines.map(function(l){var pts=l.split("：");return{meal_type:pts[0].trim()||"餐",foods:pts[1]?pts[1].trim():l.trim()}});await API.post("/api/member/meals/save",{phone:p,meals:meals,note:""});el.innerHTML="";await loadMeals()}
async function loadMeals(){var p=localStorage.getItem("fitness_phone");if(!p)return;try{var d=await API.post("/api/member/meals/list",{phone:p});renderMeals(d.meals||[])}catch(e){}}
function renderMeals(data){var el=document.getElementById("mealList");if(!data||!data.length){el.innerHTML='<div class="record-empty">还没有饮食记录</div>';return}el.innerHTML=[...data].reverse().slice(0,10).map(function(m){var h=(m.meals||[]).map(function(m2){return '<span class="meal-tag">'+(m2.meal_type||"餐")+": "+(m2.foods||"")+"</span>"}).join("");return '<div class="meal-entry"><div class="meal-entry-header"><span class="date">'+m.date+'</span></div><div>'+h+"</div></div>"}).join("")}

async function handlePhotoUpload(e){var f=e.target.files[0];if(!f)return;var p=localStorage.getItem("fitness_phone");if(!p)return;try{var du=await new Promise(function(r){var re=new FileReader();re.onload=function(){r(re.result)};re.readAsDataURL(f)});await API.post("/api/member/photos/upload",{phone:p,data_url:du,label:"第"+(P.length+1)+"次记录",note:new Date().toISOString().slice(0,10)});e.target.value="";await loadPhotos()}catch(e){}}
async function loadPhotos(){var p=localStorage.getItem("fitness_phone");if(!p)return;try{var d=await API.post("/api/member/photos/list",{phone:p});P=d.photos||[];renderPhotos()}catch(e){}}
function renderPhotos(){var el=document.getElementById("photoList");if(!P.length){el.innerHTML='<div class="record-empty">还没有照片记录</div>';return}el.innerHTML=[...P].reverse().map(function(p){return '<div class="photo-card"><img src="'+p.data_url+'" alt="'+p.label+'" loading="lazy"><div class="photo-card-info"><span class="photo-card-label">'+p.label+'</span><span class="photo-card-date">'+p.date+'</span></div>'+(p.note?'<div class="photo-card-note">'+p.note+'</div>':'')+'<div class="photo-card-delete"><button class="photo-del-btn" onclick="deletePhoto('+p.id+')">删除</button></div></div>'}).join("")}
async function deletePhoto(id){var p=localStorage.getItem("fitness_phone");if(!p||!confirm("确定删除？"))return;await API.post("/api/member/photos/delete",{phone:p,photo_id:id});await loadPhotos()}

async function handleStrengthSubmit(){var p=localStorage.getItem("fitness_phone");if(!p)return;function g(id){var v=document.getElementById(id).value.trim();return v?parseInt(v):null}var sq=g("inputSquats"),be=g("inputBench"),dl=g("inputDeadlift"),pr=g("inputPress"),pu=g("inputPullup"),no=document.getElementById("strengthNote").value.trim();if(!sq&&!be&&!dl&&!pr&&!pu){alert("请至少填一项");return}await API.post("/api/member/strength/add",{phone:p,squats:sq,bench:be,deadlift:dl,press:pr,pullup:pu,note:no});["inputSquats","inputBench","inputDeadlift","inputPress","inputPullup"].forEach(function(id){document.getElementById(id).value=""});document.getElementById("strengthNote").value="";await loadStrength()}
async function loadStrength(){var p=localStorage.getItem("fitness_phone");if(!p)return;try{var d=await API.post("/api/member/strength/list",{phone:p});S=d.entries||[];renderStrength()}catch(e){}}
function renderStrength(){var el=document.getElementById("strengthList");if(!S.length){el.innerHTML='<div class="record-empty">还没有力量数据</div>';return}el.innerHTML=[...S].reverse().map(function(e){var cells=[{label:"深蹲",val:e.squats},{label:"卧推",val:e.bench},{label:"硬拉",val:e.deadlift},{label:"推举",val:e.press},{label:"引体",val:e.pullup}];return '<div class="strength-entry"><div class="strength-entry-header"><span class="strength-entry-date">'+e.date+'</span>'+(e.note?'<span class="strength-entry-note">'+e.note+'</span>':'')+'</div><div class="strength-entry-grid">'+cells.map(function(c){return '<div class="strength-entry-item"><div class="label">'+c.label+'</div><div class="value '+(c.val===null?"empty":"")+'">'+(c.val!==null?c.val+"kg":"-")+"</div></div>"}).join("")+'</div><button class="strength-del-btn" onclick="deleteStrength('+e.id+')">删除</button></div>'}).join("")}
async function deleteStrength(id){var p=localStorage.getItem("fitness_phone");if(!p||!confirm("确定删除？"))return;await API.post("/api/member/strength/delete",{phone:p,entry_id:id});await loadStrength()}

function switchTab(t){document.querySelectorAll(".tab-btn").forEach(function(b){b.classList.remove("active")});var tb=document.querySelector('.tab-btn[data-tab="'+t+'"]');if(tb)tb.classList.add("active");document.querySelectorAll(".tab-content").forEach(function(e){e.style.display="none"});var tc=document.getElementById("tab-"+t);if(tc)tc.style.display="block";if(t==="photos")loadPhotos();if(t==="strength")loadStrength();if(t==="fatigue")loadGrip();if(t==="nutrition")loadNutrition()}

document.addEventListener("DOMContentLoaded",function(){
  var lp=document.getElementById("loginPhone");if(lp)lp.addEventListener("keydown",function(e){if(e.key==="Enter")handleLogin()});
  var cl=document.getElementById("coachLoginPhone");if(cl)cl.addEventListener("keydown",function(e){if(e.key==="Enter")handleCoachLogin()});
  var gi=document.getElementById("gripInput");if(gi)gi.addEventListener("keydown",function(e){if(e.key==="Enter")handleGripSubmit()});
  var cs=localStorage.getItem("fitness_coach"),ms=localStorage.getItem("fitness_member");
  if(cs){C=JSON.parse(cs);updateNav()}else if(ms){M=JSON.parse(ms);updateNav()}
});
"""

f=open("C:\\Users\\79018\\Documents\\体能训练资料库\\fitness_web\\static\\js\\app.js","w",encoding="utf-8")
f.write(js)
f.close()
print("OK - new JS written")
