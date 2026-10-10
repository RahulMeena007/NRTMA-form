with open("apply.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
html = re.sub(r'app_v6\.js\?v=\d+', 'app_v6.js?v=6', html)

with open("apply.html", "w", encoding="utf-8") as f:
    f.write(html)
