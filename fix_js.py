with open("app_v6.js", "r", encoding="utf-8") as f:
    js = f.read()

js = js.replace(
    "const fileInputs = ['photoUpload', 'employeeSignature', 'applicantSignature', 'medicalDocument'];",
    "const fileInputs = ['photoUpload', 'employeeSignature', 'applicantSignature', 'medicalDocument', 'filledFormDocument'];"
)

with open("app_v6.js", "w", encoding="utf-8") as f:
    f.write(js)
