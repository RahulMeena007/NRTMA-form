import re
with open("apply.html", "r", encoding="utf-8") as f:
    html = f.read()
print(re.findall(r'<input type="file" id="([^"]+)"', html))
