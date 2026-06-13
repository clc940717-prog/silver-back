import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Read current file (has everything except nutrition)
f=open("C:\\Users\\79018\\Documents\\体能训练资料库\\fitness_web\\static\\js\\app.js","r",encoding="utf-8-sig")
c=f.read()
f.close()

# Find the position before photos section 
idx = c.find("// ===== \u7167\u7247 =====")
if idx < 0:
    idx = c.find("async function handlePhotoUpload")
    
if idx > 0:
    # Insert nutrition module before photos
    nutrition_module = """
// ===== \u8425\u517b\u81b3\u98df =====
async function loadNutrition(){loadNutritionGuides();loadMeals();load52Track()}
const DAYS_CN=["\u4e00","\u4e8c","\u4e09","\u56db","\u4e94","\u516d","\u65e5"];
const DAYS_EN=["monday","tuesday","wednesday","thursday","friday","saturday","sunday"];
async function load52Track(){const p=localStorage.getItem("fitness_phone");if(!p)return;try{const d=await API.post("/api/member/52track/get",{phone:p});render52Tracker(d.track||{})}catch(e){}}
let current52Track={};
function render52Tracker(track){current52Track=track;const w=document.getElementById("f52Week");const n=document.getElementById("f52Note");if(!w)return;const t=new Date().getDay();const ti=t===0?6:t-1;w.innerHTML=DAYS_EN.map((d,i)=>{const s=track[d]||"normal";const it=i===ti;return `<div class="f52-day ${s}${it?" today":""}" onclick="toggle52Day('${d}')"><span class="day-label">${it?"\u4eca\u5929":"\u5468"+DAYS_CN[i]}</span><span class="day-icon">${s==="fast"?"\U0001f34e":"\u2705"}</span></div>`}).join("");const fd=DAYS_EN.filter(d=>track[d]==="fast").length;if(fd===0)n.textContent="\U0001f4a1 \u70b9\u51fb\u9009\u62e9\u4f60\u7684\u65ad\u98df\u65e5\uff08\u63a8\u8350\u90092\u5929\uff09";else if(fd===2)n.textContent="\u2705 \u672c\u5468 "+DAYS_EN.map((d,i)=>track[d]==="fast"?`\u5468${DAYS_CN[i]}`:"").filter(Boolean).join("\u3001")+" \u65ad\u98df \u2713";else n.textContent="\U0001f44d \u5df2\u9009 "+fd+" \u5929\uff0c\u5efa\u8bae\u90092\u5929\u6548\u679c\u6700\u4f73";}
async function toggle52Day(d){const p=localStorage.getItem("fitness_phone");if(!p)return;current52Track[d]=current52Track[d]==="fast"?"normal":"fast";render52Tracker(current52Track);await API.post("/api/member/52track/save",{phone:p,track:current52Track});}
function scrollToGuide(id){const el=document.getElementById("guideContent"+id);if(el){const card=el.closest(".nutrition-guide-card");if(card)card.classList.add("open");el.scrollIntoView({behavior:"smooth",block:"center"})}else{loadNutritionGuides().then(()=>{setTimeout(()=>{const e2=document.getElementById("guideContent"+id);if(e2){const card=e2.closest(".nutrition-guide-card");if(card)card.classList.add("open");e2.scrollIntoView({behavior:"smooth",block:"center"})}},200)})}}
async function loadNutritionGuides(){const e=document.getElementById("nutritionGuideList");if(!e)return;try{const d=await API.get("/api/nutrition/guides");e.innerHTML=d.guides.map(g=>`<div class="nutrition-guide-card" onclick="toggleGuide(${g.id})"><div class="nutrition-guide-header"><span class="nutrition-guide-icon">${g.icon}</span><span class="nutrition-guide-info"><span class="nutrition-guide-title">${g.title}</span><span class="nutrition-guide-summary">${g.summary}</span></span><span class="nutrition-guide-arrow">\u203a</span></div><div class="nutrition-guide-content" id="guideContent${g.id}">${g.content}</div></div>`).join("")}catch(e){}}
function toggleGuide(id){const card=document.getElementById("guideContent"+id).closest(".nutrition-guide-card");if(card)card.classList.toggle("open")}
async function handleMealSave(){const p=localStorage.getItem("fitness_phone");if(!p)return;const el=document.getElementById("mealInput");const m=(el.innerText||el.textContent||"").trim();if(!m){alert("\u8bf7\u8bb0\u5f55\u996e\u98df\u5185\u5bb9");return}const lines=m.split("\n").filter(l=>l.trim());const meals=lines.map(l=>{const parts=l.split("\uff1a");return{meal_type:parts[0].trim()||"\u9910",foods:parts[1]?parts[1].trim():l.trim()}});await API.post("/api/member/meals/save",{phone:p,meals:meals,note:""});el.innerHTML="";await loadMeals()}
async function loadMeals(){const p=localStorage.getItem("fitness_phone");if(!p)return;try{const d=await API.post("/api/member/meals/list",{phone:p});renderMeals(d.meals||[])}catch(e){}}
function renderMeals(data){const e=document.getElementById("mealList");if(!data||!data.length){e.innerHTML='<div class="record-empty">\u8fd8\u6ca1\u6709\u996e\u98df\u8bb0\u5f55 \U0001f957</div>';return}e.innerHTML=[...data].reverse().slice(0,10).map(m=>{const mealsHtml=(m.meals||[]).map(m2=>'<span class="meal-tag">'+(m2.meal_type||"\u9910")+": "+(m2.foods||"")+"</span>").join("");return '<div class="meal-entry"><div class="meal-entry-header"><span class="date">'+m.date+'</span></div><div>'+mealsHtml+'</div></div>'}).join("")}

"""
    c = c[:idx] + nutrition_module + c[idx:]
    f=open("C:\\Users\\79018\\Documents\\体能训练资料库\\fitness_web\\static\\js\\app.js","w",encoding="utf-8")
    f.write(c)
    f.close()
    print("OK - nutrition restored, lines:", len(c.split("\n")))
else:
    print("Could not find insertion point")
