import sys

with open("app_v6.js", "r") as f:
    code = f.read()

# 1. Add choice section elements
elements_code = """
    // UI Elements
    const choiceSection = document.getElementById("choice-section");
    const directSection = document.getElementById("direct-upload-section");
    const btnOption1 = document.getElementById("btnOption1");
    const btnOption2 = document.getElementById("btnOption2");
    const onlineBackBtn = document.getElementById("onlineBackBtn");
    const directBackBtn = document.getElementById("directBackBtn");
    const directSubmitBtn = document.getElementById("directSubmitBtn");
    
    // Switch Views
    btnOption1.addEventListener("click", () => { choiceSection.classList.add("hidden"); directSection.classList.remove("hidden"); });
    btnOption2.addEventListener("click", () => { choiceSection.classList.add("hidden"); formSection.classList.remove("hidden"); });
    onlineBackBtn.addEventListener("click", () => { formSection.classList.add("hidden"); choiceSection.classList.remove("hidden"); });
    directBackBtn.addEventListener("click", () => { directSection.classList.add("hidden"); choiceSection.classList.remove("hidden"); });

    // Direct Upload Handlers
    document.getElementById("directFileUpload").addEventListener("change", (e) => {
        if(e.target.files[0]) document.getElementById("directUploadBox").querySelector("p").innerText = e.target.files[0].name;
    });

    directSubmitBtn.addEventListener("click", async () => {
        if(!supabase) { alert("Supabase not connected"); return; }
        const pName = document.getElementById("directParticipantName").value.trim();
        const eName = document.getElementById("directEmployeeName").value.trim();
        const phone = document.getElementById("directContact").value.trim();
        const file = document.getElementById("directFileUpload").files[0];

        if(!pName || !eName || !phone || !file) { alert("Please fill all fields and select a file!"); return; }

        directSubmitBtn.innerText = "Uploading... Wait";
        directSubmitBtn.disabled = true;

        try {
            const timestamp = Date.now();
            const ext = file.name.split('.').pop();
            const path = `direct_uploads/form_${timestamp}.${ext}`;
            const { error: fErr } = await supabase.storage.from('nrtma-forms').upload(path, file);
            if(fErr) throw fErr;
            const { data: urlData } = supabase.storage.from('nrtma-forms').getPublicUrl(path);

            const { error: dbErr } = await supabase.from('applications').insert([{
                participant_name: pName,
                employee_name: eName,
                contact: phone,
                form_image_url: urlData.publicUrl,
                raw_data: { type: "direct", participantName: pName, employeeName: eName, contact: phone }
            }]);
            if(dbErr) throw dbErr;
            
            successPopup.classList.add("show");
        } catch(e) {
            console.error(e);
            alert("Error: " + e.message);
        } finally {
            directSubmitBtn.innerText = "Submit Upload";
            directSubmitBtn.disabled = false;
        }
    });
"""

code = code.replace("    // Elements", elements_code + "\n    // Elements")

# 2. Modify Online Submit Logic to upload new files
submit_find = "submitUploadBtn.addEventListener(\"click\", async () => {"
submit_replace = """submitUploadBtn.addEventListener("click", async () => {
        // Validate extra files
        const empSig = document.getElementById("employeeSignature").files[0];
        const appSig = document.getElementById("applicantSignature").files[0];
        const medDoc = document.getElementById("medicalDocument").files[0];
        
        if(!empSig || !appSig || !medDoc) {
            alert("Please upload Employee Signature, Applicant Signature, and Medical Document.");
            return;
        }
        if(medDoc.size > 2 * 1024 * 1024) {
            alert("Medical Document must be under 2MB!");
            return;
        }
"""
code = code.replace(submit_find, submit_replace)

# 3. Modify db payload
payload_find = """            if (uploadedPhotoUrl) {
                formData.photo_url = uploadedPhotoUrl;
            }
            formData.submitted_at = new Date().toISOString();"""

payload_replace = """            if (uploadedPhotoUrl) {
                formData.photo_url = uploadedPhotoUrl;
            }
            formData.type = "online";
            formData.submitted_at = new Date().toISOString();
            
            // Upload extra docs
            const uploadFile = async (f, folder) => {
                if(!f) return null;
                const path = `${folder}/${timestamp}_${f.name}`;
                await supabase.storage.from('nrtma-forms').upload(path, f);
                return supabase.storage.from('nrtma-forms').getPublicUrl(path).data.publicUrl;
            };
            
            formData.emp_signature_url = await uploadFile(empSig, "signatures");
            formData.app_signature_url = await uploadFile(appSig, "signatures");
            formData.medical_doc_url = await uploadFile(medDoc, "medical");
"""
code = code.replace(payload_find, payload_replace)

with open("app_v6.js", "w") as f:
    f.write(code)
print("Updated app_v6.js")
