with open("admin.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace('<th>Photo</th>\n', '')

with open("admin.html", "w", encoding="utf-8") as f:
    f.write(html)
