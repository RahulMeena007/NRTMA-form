with open("apply.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace('</div>\n                  </div>\n  \n                <button type="submit"', '</div>\n  \n                <button type="submit"')

with open("apply.html", "w", encoding="utf-8") as f:
    f.write(html)
