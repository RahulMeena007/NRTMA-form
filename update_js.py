with open("app_v6.js", "r", encoding="utf-8") as f:
    js = f.read()

# Replace switch view section
switch_target = """    // Switch Views
    btnOption1.addEventListener("click", () => { choiceSection.classList.add("hidden"); directSection.classList.remove("hidden"); });
    btnOption2.addEventListener("click", () => { choiceSection.classList.add("hidden"); formSection.classList.remove("hidden"); });
    onlineBackBtn.addEventListener("click", () => { formSection.classList.add("hidden"); choiceSection.classList.remove("hidden"); });
    directBackBtn.addEventListener("click", () => { directSection.classList.add("hidden"); choiceSection.classList.remove("hidden"); });"""

switch_new = """    // Switch Views
    btnOption1.addEventListener("click", () => { choiceSection.classList.add("hidden"); formSection.classList.remove("hidden"); });
    onlineBackBtn.addEventListener("click", () => { formSection.classList.add("hidden"); choiceSection.classList.remove("hidden"); });"""

js = js.replace(switch_target, switch_new)

new_logic = """
    // File uploads UI logic
    document.getElementById("photoUpload").addEventListener("change", (e) => {
        if(e.target.files[0]) document.getElementById("uploadBox").innerHTML = "<p>" + e.target.files[0].name + "</p>";
    });

    submitUploadBtn.addEventListener("click", async () => {
        if(!supabase) { alert("Supabase not connected"); return; }
        
        const inputs = [
            'trekName', 'participantName', 'employeeName', 'relation', 'designation', 
            'officeAddress', 'dob', 'doa', 'contact', 'email', 'residentialAddress', 'experience'
        ];
        
        const data = {};
        let valid = true;
        
        inputs.forEach(id => {
            const el = document.getElementById(id);
            if(!el.value.trim()) {
                el.classList.add("ap-invalid");
                valid = false;
            } else {
                el.classList.remove("ap-invalid");
                data[id] = el.value.trim();
            }
        });
        
        const emailVal = document.getElementById("email").value.trim();
        if(emailVal && !emailVal.endsWith("@gmail.com")) {
            alert("Email must be a @gmail.com address.");
            document.getElementById("email").classList.add("ap-invalid");
            valid = false;
        }
        
        const phoneVal = document.getElementById("contact").value.trim();
        if(phoneVal && !/^\\d{10}$/.test(phoneVal)) {
            alert("Mobile number must be exactly 10 digits.");
            document.getElementById("contact").classList.add("ap-invalid");
            valid = false;
        }

        const files = {
            photo: document.getElementById("photoUpload").files[0],
            empSign: document.getElementById("employeeSignature").files[0],
            appSign: document.getElementById("applicantSignature").files[0],
            medical: document.getElementById("medicalDocument").files[0],
            filledForm: document.getElementById("filledFormDocument").files[0]
        };

        if(!files.photo || !files.empSign || !files.appSign || !files.medical || !files.filledForm) {
            alert("Please select ALL 5 required files (Photo, Employee Signature, Applicant Signature, Medical Document, and Completed Form PDF/Image).");
            valid = false;
        }

        if(!valid) {
            alert("Please ensure all fields are filled perfectly.");
            return;
        }

        submitUploadBtn.innerText = "Processing & Validating... Please wait";
        submitUploadBtn.disabled = true;

        try {
            // Check uniqueness in DB
            const { data: existingData, error: fetchErr } = await supabase
                .from('applications')
                .select('id')
                .or(`contact.eq.${phoneVal},email.eq.${emailVal}`);
            
            if(fetchErr) throw fetchErr;
            if(existingData && existingData.length > 0) {
                alert("Error: An application with this mobile number or email already exists. Each application must have unique contact details.");
                throw new Error("Duplicate entry");
            }

            submitUploadBtn.innerText = "Uploading Files... Please wait";

            // Upload files
            const timestamp = Date.now();
            const urls = {};
            
            for(const [key, file] of Object.entries(files)) {
                const ext = file.name.split('.').pop();
                const path = `uploads/${key}_${timestamp}.${ext}`;
                const { error: fErr } = await supabase.storage.from('nrtma-forms').upload(path, file);
                if(fErr) throw fErr;
                const { data: urlData } = supabase.storage.from('nrtma-forms').getPublicUrl(path);
                urls[key] = urlData.publicUrl;
            }

            submitUploadBtn.innerText = "Finalizing Application...";

            // Insert DB
            const { error: dbErr } = await supabase.from('applications').insert([{
                participant_name: data.participantName,
                employee_name: data.employeeName,
                contact: phoneVal,
                email: emailVal,
                form_image_url: urls.filledForm,
                raw_data: { ...data, urls }
            }]);
            
            if(dbErr) throw dbErr;
            
            successPopup.classList.add("show");
        } catch(e) {
            console.error(e);
            if(e.message !== "Duplicate entry") alert("Error: " + e.message);
        } finally {
            submitUploadBtn.innerText = "Submit Application";
            submitUploadBtn.disabled = false;
        }
    });

    closePopupBtn.addEventListener("click", () => {
        successPopup.classList.remove("show");
        location.reload();
    });
});
"""

idx = js.find("// Direct Upload Handlers")
if idx != -1:
    js = js[:idx] + new_logic
else:
    js = js + new_logic

with open("app_v6.js", "w", encoding="utf-8") as f:
    f.write(js)
