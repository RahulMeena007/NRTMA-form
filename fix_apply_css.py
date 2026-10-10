with open("landing.css", "r", encoding="utf-8") as f:
    css = f.read()

import re
footer_css_match = re.search(r'/\* == FOOTER == \*/.*', css, flags=re.DOTALL)
if footer_css_match:
    footer_css = footer_css_match.group(0)
    
    with open("apply.css", "a", encoding="utf-8") as f:
        f.write("\n\n" + footer_css)
    print("Success")
else:
    print("Could not find footer block in landing.css")
