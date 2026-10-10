with open("app_v6.js", "r", encoding="utf-8") as f:
    js = f.read()

import re

# 1. Wire up the bottom back button
js = js.replace('const onlineBackBtn = document.getElementById("onlineBackBtn");', 
                'const onlineBackBtn = document.getElementById("onlineBackBtn");\n    const onlineBackBtnBottom = document.getElementById("onlineBackBtnBottom");')
js = js.replace('if (onlineBackBtn) {', 
                '''if (onlineBackBtn) {
        onlineBackBtnBottom.addEventListener("click", () => { 
            formSection.classList.add("hidden"); 
            choiceSection.classList.remove("hidden"); 
        });''')

# 2. Update File Inputs and Validation
js = re.sub(
    r"const fileInputs = \[.*?\];",
    "const fileInputs = ['filledFormDocument'];",
    js
)

# 3. Add 4MB Size Check
size_check = """
                if (fileEl && fileEl.files[0]) {
                    if (fileEl.files[0].size > 4 * 1024 * 1024) {
                        alert("File size for " + id + " exceeds 4 MB. Please upload a smaller PDF.");
                        valid = false;
                    } else {
                        files[id] = fileEl.files[0];
                    }
                }
"""
js = re.sub(
    r"if \(fileEl && fileEl\.files\[0\]\) \{[\s\S]*?files\[id\] = fileEl\.files\[0\];\s*\}",
    size_check.strip(),
    js
)

# 4. Update the DB Insertion to only use filledFormDocument
js = js.replace("urls.photoUpload", "urls.filledFormDocument")

with open("app_v6.js", "w", encoding="utf-8") as f:
    f.write(js)
