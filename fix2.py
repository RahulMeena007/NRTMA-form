with open("apply.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
html = re.sub(r'</div>\s*</div>\s*<button type="submit"', '</div>\n\n                <button type="submit"', html)

with open("apply.html", "w", encoding="utf-8") as f:
    f.write(html)
