with open("app_v6.js", "r", encoding="utf-8") as f:
    js = f.read()

# Replace document.addEventListener("DOMContentLoaded", () => { with a resilient version
js = js.replace('document.addEventListener("DOMContentLoaded", () => {', 'function initApp() {')
js = js.replace('});\n', '}\n\nif (document.readyState === "loading") {\n    document.addEventListener("DOMContentLoaded", initApp);\n} else {\n    initApp();\n}\n')

# Also add an alert to btnOption1 just to be super sure
js = js.replace('btnOption1.addEventListener("click", () => {', 'btnOption1.addEventListener("click", () => { \n            console.log("Start Application Clicked");')

with open("app_v6.js", "w", encoding="utf-8") as f:
    f.write(js)
