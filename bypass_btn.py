with open("apply.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
html = re.sub(r'<button id="btnOption1" class="ap-btn ap-btn-primary" style="', r'<button id="btnOption1" class="ap-btn ap-btn-primary" onclick="document.getElementById(\'choice-section\').classList.add(\'hidden\'); document.getElementById(\'form-section\').classList.remove(\'hidden\');" style="', html)

with open("apply.html", "w", encoding="utf-8") as f:
    f.write(html)
