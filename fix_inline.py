with open("apply.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
html = re.sub(r'// Photo upload preview.*?\}\);', '', html, flags=re.DOTALL)

with open("apply.html", "w", encoding="utf-8") as f:
    f.write(html)
