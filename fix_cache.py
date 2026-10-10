with open("apply.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
html = re.sub(r'<link rel="stylesheet" href="apply\.css[^"]*">', '<link rel="stylesheet" href="apply.css?v=4">', html)

with open("apply.html", "w", encoding="utf-8") as f:
    f.write(html)
