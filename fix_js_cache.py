with open("apply.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace('<script src="app_v6.js"></script>', '<script src="app_v6.js?v=2"></script>')

with open("apply.html", "w", encoding="utf-8") as f:
    f.write(html)
