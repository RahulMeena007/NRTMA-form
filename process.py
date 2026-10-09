with open("apply_backup.html", "r", encoding="utf-8") as f:
    html = f.read()

# We need to wrap the form-section so it's hidden initially, and add a choice section with an Apply Now button.
btn_html = """
        <div id="choice-section" style="display: flex; justify-content: center; width: 100%; margin-top: 40px;">
            <button id="btnOption1" class="ap-btn ap-btn-primary" style="flex: 1 1 200px; max-width: 320px; height: 60px; box-sizing: border-box; padding: 0 15px; display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 8px; transition: all 0.3s ease;">
                <span style="font-size: 22px;">??</span>
                <span style="font-size: 1rem; font-weight: 600;">Apply Now</span>
            </button>
        </div>
"""

# Replace the beginning of ap-page-wrap
html = html.replace('<div class="ap-page-wrap">', f'<div class="ap-page-wrap">\n{btn_html}')

# Hide form-section initially
html = html.replace('id="form-section"', 'id="form-section" class="ap-form-card hidden"')
# Also apply_backup.html has <div class="ap-form-card" id="form-section">, so doing replacement on id="form-section" works.
html = html.replace('class="ap-form-card" id="form-section" class="ap-form-card hidden"', 'class="ap-form-card hidden" id="form-section"')

# Add a Go Back button inside form-section
html = html.replace('<form id="nrtma-form" novalidate>', '<button id="onlineBackBtn" class="ap-btn" type="button" style="margin-bottom: 20px; background: none; color: var(--muted); border: none; padding: 0;">&larr; Back to Options</button>\n            <form id="nrtma-form" novalidate>')

with open("apply.html", "w", encoding="utf-8") as f:
    f.write(html)
