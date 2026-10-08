import sys

with open("admin.js", "r") as f:
    code = f.read()

modal_find = "const rawData = app.raw_data || {};"
modal_replace = """const rawData = app.raw_data || {};
            
            let extraDocs = "";
            if(rawData.type === "direct") {
                extraDocs = `<h4 style="margin-top: 15px;">Direct Upload</h4>
                <a href="${app.form_image_url}" target="_blank" class="btn primary-btn" style="text-decoration:none;">View Uploaded Form</a>`;
            } else if(rawData.type === "online") {
                extraDocs = `<h4 style="margin-top: 15px;">Required Documents</h4>`;
                if(rawData.emp_signature_url) extraDocs += `<br><a href="${rawData.emp_signature_url}" target="_blank" style="color: blue;">Employee Signature</a>`;
                if(rawData.app_signature_url) extraDocs += `<br><a href="${rawData.app_signature_url}" target="_blank" style="color: blue;">Applicant Signature</a>`;
                if(rawData.medical_doc_url) extraDocs += `<br><a href="${rawData.medical_doc_url}" target="_blank" style="color: blue;">Medical Document</a>`;
            }
"""
code = code.replace(modal_find, modal_replace)

modal_html_find = "modalData.innerHTML = `<ul>${details}</ul>`;"
modal_html_replace = "modalData.innerHTML = `<ul>${details}</ul>` + extraDocs;"
code = code.replace(modal_html_find, modal_html_replace)

with open("admin.js", "w") as f:
    f.write(code)
print("Updated admin.js")
