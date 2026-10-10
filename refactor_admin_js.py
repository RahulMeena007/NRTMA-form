with open("admin.js", "r", encoding="utf-8") as f:
    js = f.read()

import re

# Remove the photo logic block
photo_pattern = r'const photoSrc =.*?No Photo</span>`;'
js = re.sub(photo_pattern, '', js, flags=re.DOTALL)

# Remove the photo <td> from the HTML injected string
tr_pattern = r'<td>\s*\$\{photoHtml\}\s*</td>'
js = re.sub(tr_pattern, '', js)

# Update the "Uploaded Documents" links to ONLY show filledFormDocument
doc_html = """
                    <td>
                        <div style="display:flex; flex-direction:column; gap:5px; font-size:0.9rem;">
                        ${(rawData && rawData.urls && rawData.urls.filledFormDocument) ? `<a href="${rawData.urls.filledFormDocument}" target="_blank" style="color:#10b981; font-weight:600;">View Filled Form PDF</a>` : '<span style="color:var(--muted)">No PDF Uploaded</span>'}
                        </div>
                    </td>
"""

js = re.sub(r'<td>\s*<div style="display:flex; flex-direction:column; gap:5px; font-size:0.9rem;">.*?</div>\s*</td>', doc_html.strip(), js, flags=re.DOTALL)

with open("admin.js", "w", encoding="utf-8") as f:
    f.write(js)
