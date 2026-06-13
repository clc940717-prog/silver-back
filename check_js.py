import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
f=open("C:\\Users\\79018\\Documents\\体能训练资料库\\fitness_web\\static\\js\\app.js","r",encoding="utf-8-sig")
c=f.read()
f.close()
lines=c.split("\n")
print("Total lines:", len(lines))
print("Has nutrition:", "\u8425\u517b\u81b3\u98df" in c)
print("Has handleMealSave:", "handleMealSave" in c)
print("Has renderCurve:", "renderCurve" in c)
# Find last 3 lines
for i in range(max(0,len(lines)-5), len(lines)):
    print(f"Line {i+1}: {lines[i][:100]}")
