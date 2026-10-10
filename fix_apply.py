with open("apply.html", "r", encoding="utf-8") as f:
    html = f.read()

# Make navbar brand clickable
html = html.replace(
    '<div class="ap-nav-brand">\n            <img src="logo_1.png" alt="NRTMA Logo" class="ap-nav-logo">\n            <span>N.R.T.M.A. Portal</span>\n        </div>',
    '<a href="index.html" class="ap-nav-brand" style="text-decoration: none; color: inherit;">\n            <img src="logo_1.png" alt="NRTMA Logo" class="ap-nav-logo">\n            <span>N.R.T.M.A. Portal</span>\n        </a>'
)

# Update Apply Button section
import re
btn_pattern = r'<div id="choice-section".*?</button>\s*</div>'
better_choice_ui = """<div id="choice-section" class="ap-form-card" style="max-width: 600px; margin: 60px auto; text-align: center; padding: 60px 40px;">
            <div style="font-size: 48px; margin-bottom: 20px;">??</div>
            <h2 style="color: var(--navy); margin-bottom: 15px; font-size: 28px;">Ready to Apply?</h2>
            <p style="color: var(--muted); margin-bottom: 35px; line-height: 1.6; font-size: 16px;">Make sure you have your filled application form PDF (Max 4MB) ready to upload. Once started, please complete the form in one go.</p>
            <button id="btnOption1" class="ap-btn ap-btn-primary" style="width: 100%; max-width: 320px; height: 60px; font-size: 1.1rem; box-shadow: 0 10px 25px rgba(79, 70, 229, 0.25); display: inline-flex; align-items: center; justify-content: center; gap: 10px; transition: transform 0.2s ease;">
                <span>Start Application</span>
                <span>&rarr;</span>
            </button>
        </div>"""
html = re.sub(btn_pattern, better_choice_ui, html, flags=re.DOTALL)

with open("apply.html", "w", encoding="utf-8") as f:
    f.write(html)
