with open("apply.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    # Skip direct-upload-section
    if 'id="direct-upload-section"' in line:
        skip = True
        continue
    if skip and '<!-- ONLINE FORM CARD (OPTION 2) -->' in line:
        skip = False

    if skip:
        continue
        
    # Replace choice buttons
    if 'id="btnOption1"' in line:
        new_lines.append('                <button id="btnOption1" class="ap-btn ap-btn-outline" style="flex: 1 1 200px; width: 100%; max-width: 320px; height: 60px; box-sizing: border-box; padding: 0 15px; display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 8px; border: 2px solid var(--blue); transition: all 0.3s ease;">\n')
        new_lines.append('                    <span style="font-size: 22px; color: var(--blue);">??</span>\n')
        new_lines.append('                    <span style="font-size: 1rem; font-weight: 600;">Upload Filled Form</span>\n')
        new_lines.append('                </button>\n')
        continue
    
    if '<span style="font-size: 24px; color: var(--blue);">??</span>' in line or '<span style="font-size: 1.1rem; font-weight: 600;">Upload Direct Pdf</span>' in line or '<button id="btnOption2"' in line or 'Fill Form Online' in line and not 'Upload Filled' in line:
        continue
        
    if '<a href="https://nr.indianrailways.gov.in/view_section.jsp' in line:
        new_lines.append('                <a href="https://nr.indianrailways.gov.in/view_section.jsp?fontColor=black&backgroundColor=LIGHTSTEELBLUE&lang=0&id=0,4,366" target="_blank" class="ap-btn ap-btn-primary" style="flex: 1 1 200px; width: 100%; max-width: 320px; height: 60px; box-sizing: border-box; padding: 0 15px; text-decoration: none; display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 8px; border: 2px solid transparent; transition: all 0.3s ease;">\n')
        new_lines.append('                    <span style="font-size: 22px;">??</span>\n')
        new_lines.append('                    <span style="font-size: 1rem; font-weight: 600;">Apply Online</span>\n')
        new_lines.append('                </a>\n')
        continue
        
    if '<span style="font-size: 24px;">??</span>' in line or '<span style="font-size: 1.1rem; font-weight: 600;">Apply Online</span>' in line:
        continue
        
    # Make all inputs compulsory
    if '<label for="officeAddress">5. Office Address</label>' in line:
        line = line.replace('</label>', ' <span class="req">*</span></label>')
    if '<label for="dob">6. Date of Birth (Participant)</label>' in line:
        line = line.replace('</label>', ' <span class="req">*</span></label>')
    if '<label for="doa">7. Date of Appointment (Employee)</label>' in line:
        line = line.replace('</label>', ' <span class="req">*</span></label>')
    if '<label for="residentialAddress">9. Residential Address</label>' in line:
        line = line.replace('</label>', ' <span class="req">*</span></label>')
    if '<label for="experience">10. Experience in Adventure Activities (if any)</label>' in line:
        line = line.replace('</label>', ' <span class="req">*</span></label>')
        
    # Add Filled Form upload option right after Medical Document
    if 'id="medicalDocument"' in line:
        new_lines.append(line)
        new_lines.append('                        </div>\n')
        new_lines.append('                        <div class="ap-field ap-span-2">\n')
        new_lines.append('                            <label>Completed Application Form (PDF or Image) <span class="req">*</span></label>\n')
        new_lines.append('                            <input type="file" id="filledFormDocument" accept="image/*,.pdf" style="padding: 10px; border: 1px solid var(--border); width: 100%; border-radius: 8px; height: 44px; background: #f8fafc;">\n')
        continue
        
    # Change Preview button to Submit Upload
    if 'id="previewBtn"' in line:
        line = '                    <button type="button" id="submitUploadBtn" class="ap-btn ap-btn-primary" style="width: 100%; margin-top: 30px;">Submit Application</button>\n'
        
    new_lines.append(line)

final_text = "".join(new_lines)
final_text = final_text.split("<!-- ----- PREVIEW SECTION ----- -->")[0] + "        <!-- SUCCESS POPUP -->\n" + final_text.split("<!-- SUCCESS POPUP -->")[1]

with open("apply.html", "w", encoding="utf-8") as f:
    f.write(final_text)
