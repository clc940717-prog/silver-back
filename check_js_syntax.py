import re
f=open("C:\\Users\\79018\\Documents\\体能训练资料库\\fitness_web\\static\\js\\app.js","r",encoding="utf-8")
c=f.read()
f.close()

# Check for \u not followed by 4 hex digits
for m in re.finditer(r"\\u[0-9a-fA-F]{0,3}([^0-9a-fA-F\"\\]|$)", c):
    start = max(0, m.start()-20)
    print(f"Bad escape at line {c[:m.start()].count(chr(10))+1}: ...{c[max(0,m.start()-30):m.end()+10]}...")
    break
else:
    print("All \\u escapes valid")
print(f"File size: {len(c)} chars, {c.count(chr(10))+1} lines")
