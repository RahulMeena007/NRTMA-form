with open("apply.html", "r", encoding="utf-8") as f:
    html = f.read()

import re

# 1. Replace Uploads Section
upload_section_pattern = r'<!-- UPLOADS SECTION -->.*?</div>\s*</div>'
new_upload_section = """<!-- UPLOADS SECTION -->
                <div class="ap-section-group" style="margin-top: 30px; background: #f8fafc; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0;">
                    <h3 style="margin-bottom: 20px; font-size: 1.1rem; color: var(--navy);">Required Documents</h3>
                    <div class="ap-form-grid">
                        <div class="ap-field ap-span-2">
                            <label>Upload Filled Form (PDF only, Max 4MB) <span class="req">*</span></label>
                            <input type="file" id="filledFormDocument" accept=".pdf" style="padding: 10px; border: 1px solid var(--border); width: 100%; border-radius: 8px; background: white;" data-required="true">
                        </div>
                    </div>
                </div>"""
html = re.sub(upload_section_pattern, new_upload_section, html, flags=re.DOTALL)

# 2. Add Back Button below Submit
submit_pattern = r'<button type="submit" id="submitBtn".*?Submit Application</button>'
new_buttons = """<button type="submit" id="submitBtn" class="ap-btn ap-btn-primary" style="width: 100%; margin-top: 30px; padding: 15px; font-size: 18px;">Submit Application</button>
                <button type="button" id="onlineBackBtnBottom" class="ap-btn" style="width: 100%; margin-top: 15px; background: none; color: var(--muted); border: 2px solid var(--border); padding: 15px; font-size: 18px;">&larr; Go Back</button>"""
html = re.sub(submit_pattern, new_buttons, html)

with open("apply.html", "w", encoding="utf-8") as f:
    f.write(html)
