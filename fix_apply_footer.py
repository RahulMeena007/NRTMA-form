with open("apply.css", "r", encoding="utf-8") as f:
    css = f.read()

import re

# Remove the broken imported footer styles
css = re.sub(r'/\* Imported Footer Styles from landing\.css \*/.*', '', css, flags=re.DOTALL)

# Add the correct footer styles
correct_footer_css = """
/* Imported Footer Styles from landing.css */
.footer { background: var(--navy); color: #94a3b8; }
.footer-main {
    display: grid; grid-template-columns: 1.5fr 1fr 1fr 1fr;
    gap: 40px; max-width: 1200px; margin: 0 auto; padding: 60px 40px 40px;
}
.footer-brand { display: flex; gap: 16px; margin-bottom: 16px; }
.footer-brand-logo { height: 44px; opacity: .85; }
.footer-col h4 { font-family: var(--font-head); font-size: 1.3rem; color: var(--white); margin-bottom: 12px; }
.footer-col h5 {
    font-family: var(--font-head); font-size: 1rem; color: var(--white);
    margin-bottom: 16px; padding-bottom: 10px;
    border-bottom: 2px solid rgba(255,255,255,.08);
}
.footer-col p { font-size: .88rem; margin-bottom: 12px; line-height: 1.7; }
.footer-col strong { color: #cbd5e1; }
.footer-col ul { list-style: none; padding-left: 0; }
.footer-col li { margin-bottom: 10px; }
.footer-col a {
    color: #94a3b8; text-decoration: none; font-size: .9rem; transition: color .2s;
}
.footer-col a:hover { color: #60a5fa; }
.footer-bottom {
    border-top: 1px solid rgba(255,255,255,.06);
    max-width: 1200px; margin: 0 auto; padding: 20px 40px;
    text-align: center;
}
.footer-bottom p { font-size: .82rem; color: #475569; }
.footer-bottom p:first-child { color: #cbd5e1; font-weight: 600; margin-bottom: 8px; }
.footer-disclaimer { max-width: 800px; margin: 0 auto; line-height: 1.6; }

@media (max-width: 900px) {
    .footer-main { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 600px) {
    .footer-main { grid-template-columns: 1fr; padding: 40px 20px 20px; }
    .footer-bottom { padding: 20px; }
}
"""

with open("apply.css", "w", encoding="utf-8") as f:
    f.write(css + correct_footer_css)
