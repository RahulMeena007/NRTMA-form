with open("index.html", "r", encoding="utf-8") as f:
    index_html = f.read()

import re
footer_match = re.search(r'<footer class="site-footer">.*?</footer>', index_html, flags=re.DOTALL)
if footer_match:
    full_footer = footer_match.group(0)
    
    with open("apply.html", "r", encoding="utf-8") as f:
        apply_html = f.read()
    
    # Remove ?? and replace with SVG icon
    icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 20px;"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>"""
    apply_html = apply_html.replace('<div style="font-size: 48px; margin-bottom: 20px;">??</div>', icon_svg)
    apply_html = apply_html.replace('<div style="font-size: 48px; margin-bottom: 20px;">??</div>', icon_svg)

    # Replace the old minimal footer
    old_footer_pattern = r'<footer class="ap-footer">.*?</footer>'
    apply_html = re.sub(old_footer_pattern, full_footer, apply_html, flags=re.DOTALL)

    with open("apply.html", "w", encoding="utf-8") as f:
        f.write(apply_html)
    print("Success")
else:
    print("Footer not found in index.html")
