with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Make navbar brand clickable
html = html.replace(
    '<div class="ap-nav-brand">\n            <img src="logo_1.png" alt="NRTMA Logo" class="ap-nav-logo">\n            <span>N.R.T.M.A. Portal</span>\n        </div>',
    '<a href="index.html" class="ap-nav-brand" style="text-decoration: none; color: inherit;">\n            <img src="logo_1.png" alt="NRTMA Logo" class="ap-nav-logo">\n            <span>N.R.T.M.A. Portal</span>\n        </a>'
)

# Update Camp 8
html = html.replace('Last date to apply: 08 Oct 2026', 'Last date to apply: 30 Oct 2026')
html = html.replace('data-date="2026-10-08T23:59:59"', 'data-date="2026-10-30T23:59:59"')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
