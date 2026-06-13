f=open("C:\\Users\\79018\\Documents\\体能训练资料库\\fitness_web\\templates\\index.html","r",encoding="utf-8")
c=f.read()
f.close()

# 1. Replace training records tab content
old_records='''            <!-- 训练记录 -->
            <div class="tab-content active" id="tab-records"><div class="record-list" id="recordList"></div></div>'''
# Keep as is, JS will handle RPE rendering

# 2. Replace fatigue tab to add curve section at top
old_fatigue='''            <!-- 疲劳管理 -->
            <div class="tab-content" id="tab-fatigue" style="display:none">
                <div class="grip-area">
                    <div id="gripStatusContainer"></div>
                    <div class="grip-info-card"><strong>💡 为什么用握力测疲劳？</strong><br>握力是中枢神经系统疲劳的敏感指标。每天早晨用握力计测量，如果数值比你的基线下降超过5%，说明身体未完全恢复，建议调整今日训练强度。</div>
                    <div class="grip-input-card">
                        <div class="grip-input-title">🤚 记录今日握力</div>
                        <div class="grip-input-row"><input class="grip-input" id="gripInput" type="number" step="0.1" placeholder="0.0" inputmode="decimal"><span class="grip-input-unit">kg</span></div>
                        <input class="grip-input-note" id="gripNote" type="text" placeholder="晨起状态（选填）">
                        <button class="grip-submit" onclick="handleGripSubmit()">记录</button>
                    </div>
                    <div style="font-size:14px;font-weight:600;color:rgba(255,255,255,0.5);margin-bottom:12px">📊 历史趋势</div>
                    <div id="gripList"></div>
                </div>
            </div>'''

new_fatigue='''            <!-- 疲劳管理 -->
            <div class="tab-content" id="tab-fatigue" style="display:none">
                <div class="grip-area">
                    <div id="gripStatusContainer"></div>
                    <div class="fatigue-curve" id="fatigueCurveSection">
                        <div class="fatigue-curve-title">📈 疲劳曲线 <span>结合握力 + 训练RPE</span></div>
                        <div class="curve-chart" id="curveChart">
                            <div class="curve-empty">记录握力和RPE后自动生成</div>
                        </div>
                        <div class="curve-legend">
                            <span><span class="legend-dot" style="background:#22c55e"></span> 握力正常</span>
                            <span><span class="legend-dot" style="background:#eab308"></span> 轻度疲劳</span>
                            <span><span class="legend-dot" style="background:#ef4444"></span> 高度疲劳</span>
                            <span><span class="legend-dot" style="background:#4b88ff;width:6px;height:6px;border-radius:50%"></span> RPE评分</span>
                        </div>
                    </div>
                    <div class="grip-info-card"><strong>💡 为什么用握力测疲劳？</strong><br>握力是中枢神经系统疲劳的敏感指标。每天早晨用握力计测量，如果数值比你的基线下降超过5%，说明身体未完全恢复，建议调整今日训练强度。</div>
                    <div class="grip-input-card">
                        <div class="grip-input-title">🤚 记录今日握力</div>
                        <div class="grip-input-row"><input class="grip-input" id="gripInput" type="number" step="0.1" placeholder="0.0" inputmode="decimal"><span class="grip-input-unit">kg</span></div>
                        <input class="grip-input-note" id="gripNote" type="text" placeholder="晨起状态（选填）">
                        <button class="grip-submit" onclick="handleGripSubmit()">记录</button>
                    </div>
                    <div style="font-size:14px;font-weight:600;color:rgba(255,255,255,0.5);margin-bottom:12px">\U0001f4ca 握力趋势</div>
                    <div id="gripList"></div>
                </div>
            </div>'''

if old_fatigue in c:
    c=c.replace(old_fatigue,new_fatigue)
    f=open("C:\\Users\\79018\\Documents\\体能训练资料库\\fitness_web\\templates\\index.html","w",encoding="utf-8")
    f.write(c)
    f.close()
    print("OK - fatigue replaced")
else:
    print("NOT FOUND")
    idx=c.find("tab-fatigue")
    if idx>=0: print(c[idx:idx+300])
