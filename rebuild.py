import re

with open("apply.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Choice Section
choice_target = '<div style="display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; width: 100%;">'
choice_end = '</div>\n        </div>\n\n        <!-- DIRECT UPLOAD CARD'
choice_new = '''<div style="display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; width: 100%;">
                <button id="btnOption1" class="ap-btn ap-btn-outline" style="flex: 1 1 200px; width: 100%; max-width: 320px; height: 60px; box-sizing: border-box; padding: 0 15px; display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 8px; border: 2px solid var(--blue); transition: all 0.3s ease;">
                    <span style="font-size: 22px; color: var(--blue);">??</span>
                    <span style="font-size: 1rem; font-weight: 600;">Upload Filled Form</span>
                </button>
                <a href="https://nr.indianrailways.gov.in/view_section.jsp?fontColor=black&backgroundColor=LIGHTSTEELBLUE&lang=0&id=0,4,366" target="_blank" class="ap-btn ap-btn-primary" style="flex: 1 1 200px; width: 100%; max-width: 320px; height: 60px; box-sizing: border-box; padding: 0 15px; text-decoration: none; display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 8px; border: 2px solid transparent; transition: all 0.3s ease;">
                    <span style="font-size: 22px;">??</span>
                    <span style="font-size: 1rem; font-weight: 600;">Apply Online</span>
                </a>
            </div>
        </div>

        <!-- ONLINE FORM CARD'''

idx_start = html.find(choice_target)
idx_end = html.find(choice_end)
if idx_start != -1 and idx_end != -1:
    html = html[:idx_start] + choice_new + html[idx_end+len(choice_end)-23:]

# 2. Remove direct-upload-section
html = re.sub(r'<!-- DIRECT UPLOAD CARD \(OPTION 1\) -->.*?<!-- ONLINE FORM CARD \(OPTION 2\) -->', '<!-- ONLINE FORM CARD -->', html, flags=re.DOTALL)

# 3. Add Filled Form upload to form
form_upload_target = '''<div class="ap-field">
                            <label>Medical Document (Under 2MB) <span class="req">*</span></label>
                            <input type="file" id="medicalDocument" accept="image/*,.pdf" style="padding: 10px; border: 1px solid var(--border); width: 100%; border-radius: 8px; height: 44px; background: #f8fafc;">
                        </div>'''
form_upload_new = form_upload_target + '''
                        <div class="ap-field ap-span-2">
                            <label>Completed Application Form (PDF or Image) <span class="req">*</span></label>
                            <input type="file" id="filledFormDocument" accept="image/*,.pdf" style="padding: 10px; border: 1px solid var(--border); width: 100%; border-radius: 8px; height: 44px; background: #f8fafc;">
                        </div>'''
html = html.replace(form_upload_target, form_upload_new)

# 4. Make all labels mandatory
html = html.replace('<label for="officeAddress">5. Office Address</label>', '<label for="officeAddress">5. Office Address <span class="req">*</span></label>')
html = html.replace('<label for="dob">6. Date of Birth (Participant)</label>', '<label for="dob">6. Date of Birth (Participant) <span class="req">*</span></label>')
html = html.replace('<label for="doa">7. Date of Appointment (Employee)</label>', '<label for="doa">7. Date of Appointment (Employee) <span class="req">*</span></label>')
html = html.replace('<label for="residentialAddress">9. Residential Address</label>', '<label for="residentialAddress">9. Residential Address <span class="req">*</span></label>')
html = html.replace('<label for="experience">10. Experience in Adventure Activities (if any)</label>', '<label for="experience">10. Experience in Adventure Activities (if any) <span class="req">*</span></label>')

# 5. Remove Preview button & add Submit Upload button
preview_target = '''<button type="button" id="previewBtn" class="ap-btn ap-btn-primary" style="width: 100%; margin-top: 30px;">Preview Form &rarr;</button>'''
preview_new = '''<button type="button" id="submitUploadBtn" class="ap-btn ap-btn-primary" style="width: 100%; margin-top: 30px;">Submit Application</button>'''
html = html.replace(preview_target, preview_new)

# 6. Remove PREVIEW SECTION
html = re.sub(r'<!-- ----- PREVIEW SECTION ----- -->.*?(?=<!-- SUCCESS POPUP -->)', '', html, flags=re.DOTALL)

with open("apply.html", "w", encoding="utf-8") as f:
    f.write(html)
