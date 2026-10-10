with open("admin.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace('<th>Generated Form</th>', '<th>Uploaded Documents</th>')

with open("admin.html", "w", encoding="utf-8") as f:
    f.write(html)


with open("admin.js", "r", encoding="utf-8") as f:
    js = f.read()

# Fix the photo extraction
js = js.replace(
    'const photoSrc = (rawData && rawData.photo_url) ? rawData.photo_url : \'\';',
    'const photoSrc = (rawData && rawData.urls && rawData.urls.photoUpload) ? rawData.urls.photoUpload : (rawData.photo_url || \'\');'
)

# Fix the "Generated Form" link extraction
doc_html = """
                    <td>
                        <div style="display:flex; flex-direction:column; gap:5px; font-size:0.9rem;">
                        ${(rawData && rawData.urls && rawData.urls.medicalDocument) ? `<a href="${rawData.urls.medicalDocument}" target="_blank" style="color:#0ea5e9;">Medical Doc</a>` : ''}
                        ${(rawData && rawData.urls && rawData.urls.applicantSignature) ? `<a href="${rawData.urls.applicantSignature}" target="_blank" style="color:#0ea5e9;">App Sign</a>` : ''}
                        ${(rawData && rawData.urls && rawData.urls.employeeSignature) ? `<a href="${rawData.urls.employeeSignature}" target="_blank" style="color:#0ea5e9;">Emp Sign</a>` : ''}
                        ${(rawData && rawData.urls && rawData.urls.filledForm) ? `<a href="${rawData.urls.filledForm}" target="_blank" style="color:#10b981; font-weight:600;">Filled Form</a>` : ''}
                        </div>
                    </td>
"""

js = js.replace('''                    <td>
                        ${row.form_image_url 
                            ? `<a href="${row.form_image_url}" target="_blank" style="color: #4f46e5; font-weight: 500;">View Form Image</a>` 
                            : 'No Image'}
                    </td>''', doc_html)

with open("admin.js", "w", encoding="utf-8") as f:
    f.write(js)
