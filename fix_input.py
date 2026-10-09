with open("apply.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
idx = html.find('id="medicalDocument"')
if idx != -1:
    end_div = html.find('</div>', idx)
    insertion = '''
                        <div class="ap-field ap-span-2">
                            <label>Completed Application Form (PDF or Image) <span class="req">*</span></label>
                            <input type="file" id="filledFormDocument" accept="image/*,.pdf" style="padding: 10px; border: 1px solid var(--border); width: 100%; border-radius: 8px; height: 44px; background: #f8fafc;">
                        </div>'''
    html = html[:end_div+6] + insertion + html[end_div+6:]
    with open("apply.html", "w", encoding="utf-8") as f:
        f.write(html)
        print("Success")
