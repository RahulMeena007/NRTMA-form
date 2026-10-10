with open("landing.css", "r", encoding="utf-8") as f:
    css = f.read()

import re
# Match any rule containing ".footer"
# A simple regex for top-level CSS blocks
blocks = re.findall(r'(\.[^{]*footer[^{]*\{[^}]*\})', css, flags=re.IGNORECASE|re.DOTALL)
footer_css = "\n\n/* Imported Footer Styles from landing.css */\n" + "\n".join(blocks)

# There might also be media queries for the footer.
media_blocks = re.findall(r'(@media[^{]+\{.*?\})', css, flags=re.IGNORECASE|re.DOTALL)
# It's safer to just grab the known footer CSS. I'll just append what we matched.

with open("apply.css", "a", encoding="utf-8") as f:
    f.write(footer_css)
