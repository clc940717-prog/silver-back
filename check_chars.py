import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
f=open("C:\\Users\\79018\\Documents\\体能训练资料库\\fitness_web\\static\\js\\app.js","r",encoding="utf-8")
c=f.read()
f.close()
# Check for any chars outside ASCII range that aren't valid JS identifiers
# Find any suspicious characters
for i, ch in enumerate(c):
    if ord(ch) > 127 and ord(ch) < 0x2000 and ch not in '·×→✦✓✕●▸●▪　—━│•★☆✓✕✗✘✙✚✛✜✝✞✟✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓':
        line = c[:i].count("\n") + 1
        context_start = max(0, i-20)
        context_end = min(len(c), i+20)
        context = c[context_start:context_end].replace("\n"," ")
        print(f"Char U+{ord(ch):04X} at line {line}, pos {i}: ...{context}...")
        break
else:
    print("No suspicious chars found")
