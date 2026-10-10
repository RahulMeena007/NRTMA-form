with open("apply.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
html = re.sub(r'<button id="onlineBackBtn" class="ap-btn" type="button" style="', r'<button id="onlineBackBtn" class="ap-btn" type="button" onclick="document.getElementById(\'form-section\').classList.add(\'hidden\'); document.getElementById(\'choice-section\').classList.remove(\'hidden\');" style="', html)

html = re.sub(r'<button type="button" id="onlineBackBtnBottom" class="ap-btn" style="', r'<button type="button" id="onlineBackBtnBottom" class="ap-btn" onclick="document.getElementById(\'form-section\').classList.add(\'hidden\'); document.getElementById(\'choice-section\').classList.remove(\'hidden\');" style="', html)

with open("apply.html", "w", encoding="utf-8") as f:
    f.write(html)
