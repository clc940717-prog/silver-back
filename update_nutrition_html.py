f=open("C:\\Users\\79018\\Documents\\体能训练资料库\\fitness_web\\templates\\index.html","r",encoding="utf-8")
c=f.read()
f.close()

old = """<!-- 营养膳食 -->
            <div class="tab-content" id="tab-nutrition" style="display:none">
                <div class="nutrition-area">
                    <div class="section-label" style="margin-bottom:16px">NUTRITION</div>
                    <div id="nutritionGuideList"></div>
                    <div class="nutrition-meal-form">
                        <div class="coach-write-title" style="color:#22c55e">🥗 今日饮食记录</div>
                        <div class="coach-write-textarea" id="mealInput" contenteditable="true" style="min-height:80px;white-space:pre-line" placeholder="记录你今天吃了什么...&#10;早餐：&#10;午餐：&#10;晚餐："></div>
                        <button class="strength-submit" onclick="handleMealSave()" style="margin-top:8px">保存饮食记录</button>
                    </div>
                    <div style="font-size:14px;font-weight:600;color:rgba(255,255,255,0.5);margin:20px 0 12px;padding-top:8px">📋 饮食历史</div>
                    <div id="mealList"></div>
                </div>
            </div>"""

new = """<!-- 营养膳食 -->
            <div class="tab-content" id="tab-nutrition" style="display:none">
                <div class="nutrition-area">
                    <div class="nutrition-spotlight">
                        <div class="nutrition-spotlight-badge">\u2b50 教练推荐</div>
                        <div class="nutrition-spotlight-title">5:2 轻断食</div>
                        <div class="nutrition-spotlight-desc">这是我最推荐给会员的饮食方案。每周5天正常吃，选2天适度控制热量，简单、有效、容易坚持。</div>
                        <button class="nutrition-spotlight-btn" onclick="scrollToGuide(1)">了解详情 \u2192</button>
                    </div>
                    <div class="f52-tracker" id="f52Tracker">
                        <div class="f52-tracker-title">\U0001f4c5 本周断食计划 <span>点击标记断食日</span></div>
                        <div class="f52-week" id="f52Week"></div>
                        <div class="f52-note" id="f52Note">点击日期切换 正常 \u2194 断食</div>
                    </div>
                    <div class="meal-log-area">
                        <div class="meal-section-title">\U0001f957 今日饮食记录</div>
                        <div class="meal-input-area" id="mealInput" contenteditable="true" data-placeholder="\u8bb0\u5f55\u4f60\u4eca\u5929\u5403\u4e86\u4ec0\u4e48...\n\u65e9\u9910\uff1a\n\u5348\u9910\uff1a\n\u665a\u9910\uff1a\n\u52a0\u9910\uff1a"></div>
                        <button class="meal-submit" onclick="handleMealSave()">保存饮食记录</button>
                    </div>
                    <div class="meal-history-title">\U0001f4cb 饮食历史</div>
                    <div id="mealList"></div>
                    <div class="meal-history-title" style="margin-top:24px">\U0001f4d6 营养知识</div>
                    <div class="guide-list" id="nutritionGuideList"></div>
                </div>
            </div>"""

if old in c:
    c = c.replace(old, new)
    f=open("C:\\Users\\79018\\Documents\\体能训练资料库\\fitness_web\\templates\\index.html","w",encoding="utf-8")
    f.write(c)
    f.close()
    print("OK - replaced")
else:
    print("NOT FOUND")
    # Debug: print first 100 chars around "营养膳食"
    idx = c.find("营养膳食")
    if idx >= 0:
        print(c[idx:idx+200])
