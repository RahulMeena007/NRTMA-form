with open("apply.css", "r", encoding="utf-8") as f:
    css = f.read()

css = css.replace(':root {', ':root {\n      --navy: #0f172a;\n      --white: #ffffff;\n      --font-head: \'Outfit\', sans-serif;')

with open("apply.css", "w", encoding="utf-8") as f:
    f.write(css)
