with open("apply.html", "r", encoding="utf-8") as f:
    html = f.read()

import re

# Fix button emoji
html = html.replace('??', '')

form_html = """
        <div class="ap-form-card hidden" id="form-section" style="max-width: 900px; margin: 0 auto;">
            <button id="onlineBackBtn" class="ap-btn" type="button" style="margin-bottom: 20px; background: none; color: var(--muted); border: none; padding: 0; font-size: 16px;">&larr; Go Back</button>
            <form id="nrtma-form" novalidate style="text-align: left;">
                
                <h2 style="text-align: center; color: var(--navy); margin-bottom: 10px;">Application Form</h2>
                <p style="text-align: center; color: var(--muted); margin-bottom: 30px;">Fill the form exactly as per NRTMA application guidelines.</p>

                <div class="ap-form-grid">
                    <div class="ap-field ap-span-2">
                        <label for="trekName">Name of trek/activity applied for <span class="req">*</span></label>
                        <input type="text" id="trekName" name="trekName" placeholder="e.g. Trekking Camp" data-required="true">
                    </div>
                    <div class="ap-field">
                        <label for="participantName">1. NAME OF PARTICIPANT <span class="req">*</span></label>
                        <input type="text" id="participantName" name="participantName" placeholder="Participant Name" data-required="true">
                    </div>
                    <div class="ap-field">
                        <label for="employeeName">2. Name of employee <span class="req">*</span></label>
                        <input type="text" id="employeeName" name="employeeName" placeholder="Employee Name" data-required="true">
                    </div>
                    <div class="ap-field">
                        <label for="relation">3. Relation with Rly. employee <span class="req">*</span></label>
                        <input type="text" id="relation" name="relation" placeholder="Self / Spouse / Child" data-required="true">
                    </div>
                    <div class="ap-field">
                        <label for="designation">4. Designation of employee <span class="req">*</span></label>
                        <input type="text" id="designation" name="designation" placeholder="Designation" data-required="true">
                    </div>
                    <div class="ap-field ap-span-2">
                        <label for="officeAddress">5. Office address <span class="req">*</span></label>
                        <input type="text" id="officeAddress" name="officeAddress" placeholder="Office Address" data-required="true">
                    </div>
                    <div class="ap-field">
                        <label for="dob">6. DOB (of participant) <span class="req">*</span></label>
                        <input type="date" id="dob" name="dob" data-required="true">
                    </div>
                    <div class="ap-field">
                        <label for="doa">DOA (of employee) <span class="req">*</span></label>
                        <input type="date" id="doa" name="doa" data-required="true">
                    </div>
                    <div class="ap-field">
                        <label for="contact">7. Contact no(s) <span class="req">*</span></label>
                        <input type="tel" id="contact" name="contact" placeholder="10-digit mobile number" data-required="true">
                    </div>
                    <div class="ap-field">
                        <label for="email">E-mail <span class="req">*</span></label>
                        <input type="email" id="email" name="email" placeholder="example@gmail.com" data-required="true">
                    </div>
                    <div class="ap-field ap-span-2">
                        <label for="residentialAddress">8. Residential address <span class="req">*</span></label>
                        <input type="text" id="residentialAddress" name="residentialAddress" placeholder="Full residential address" data-required="true">
                    </div>
                    <div class="ap-field ap-span-2">
                        <label for="experience">9. Experience in any adventure / NRTMA camps (with doc proof), if any</label>
                        <input type="text" id="experience" name="experience" placeholder="Describe experience">
                    </div>
                </div>

                <!-- UPLOADS SECTION -->
                <div class="ap-section-group" style="margin-top: 30px; background: #f8fafc; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0;">
                    <h3 style="margin-bottom: 20px; font-size: 1.1rem; color: var(--navy);">Required Documents (Photos/Scans)</h3>
                    <div class="ap-form-grid">
                        <div class="ap-field">
                            <label>Passport Size Photo <span class="req">*</span></label>
                            <input type="file" id="photoUpload" accept="image/*" style="padding: 10px; border: 1px solid var(--border); width: 100%; border-radius: 8px; background: white;" data-required="true">
                        </div>
                        <div class="ap-field">
                            <label>Signature of Employee <span class="req">*</span></label>
                            <input type="file" id="employeeSignature" accept="image/*" style="padding: 10px; border: 1px solid var(--border); width: 100%; border-radius: 8px; background: white;" data-required="true">
                        </div>
                        <div class="ap-field">
                            <label>Signature of Applicant <span class="req">*</span></label>
                            <input type="file" id="applicantSignature" accept="image/*" style="padding: 10px; border: 1px solid var(--border); width: 100%; border-radius: 8px; background: white;" data-required="true">
                        </div>
                        <div class="ap-field">
                            <label>Medical Certificate of Participant <span class="req">*</span></label>
                            <input type="file" id="medicalDocument" accept="image/*,.pdf" style="padding: 10px; border: 1px solid var(--border); width: 100%; border-radius: 8px; background: white;" data-required="true">
                        </div>
                    </div>
                </div>

                <button type="submit" id="submitBtn" class="ap-btn ap-btn-primary" style="width: 100%; margin-top: 30px; padding: 15px; font-size: 18px;">Submit Application</button>
            </form>
        </div>
"""

start_idx = html.find('<div class="ap-form-card hidden" id="form-section">')
if start_idx == -1:
    start_idx = html.find('<div class="ap-form-card" id="form-section">')

end_idx = html.find('</div><!-- /ap-page-wrap -->')

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + form_html + "\n    " + html[end_idx:]

with open("apply.html", "w", encoding="utf-8") as f:
    f.write(html)
