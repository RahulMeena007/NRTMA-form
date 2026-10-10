with open("admin.js", "r", encoding="utf-8") as f:
    js = f.read()

js = js.replace("rawData.urls.filledForm", "rawData.urls.filledFormDocument")

with open("admin.js", "w", encoding="utf-8") as f:
    f.write(js)
