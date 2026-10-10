js = """
document.addEventListener("DOMContentLoaded", () => {
    const btnOption1 = document.getElementById("btnOption1");
    const choiceSection = document.getElementById("choice-section");
    const formSection = document.getElementById("form-section");
    const onlineBackBtn = document.getElementById("onlineBackBtn");
    const submitBtn = document.getElementById("submitBtn");
    const successPopup = document.getElementById("successPopup");
    const closePopupBtn = document.getElementById("closePopupBtn");

    if (btnOption1) {
        btnOption1.addEventListener("click", () => { 
            choiceSection.classList.add("hidden"); 
            formSection.classList.remove("hidden"); 
        });
    }
    
    if (onlineBackBtn) {
        onlineBackBtn.addEventListener("click", () => { 
            formSection.classList.add("hidden"); 
            choiceSection.classList.remove("hidden"); 
        });
    }

    if (submitBtn) {
        submitBtn.addEventListener("click", async (e) => {
            e.preventDefault();
            
            const inputs = [
                'trekName', 'participantName', 'employeeName', 'relation', 'designation', 
                'officeAddress', 'dob', 'doa', 'contact', 'email', 'residentialAddress', 'experience'
            ];
            
            const data = {};
            let valid = true;
            
            inputs.forEach(id => {
                const el = document.getElementById(id);
                if(el && el.hasAttribute('data-required') && !el.value.trim()) {
                    el.classList.add("ap-invalid");
                    valid = false;
                } else if(el) {
                    el.classList.remove("ap-invalid");
                    data[id] = el.value.trim();
                }
            });

            // Validate Email and Phone
            const emailVal = data.email || "";
            if(emailVal && !emailVal.endsWith("@gmail.com")) {
                alert("Email must be a @gmail.com address.");
                document.getElementById("email").classList.add("ap-invalid");
                valid = false;
            }
            
            const phoneVal = data.contact || "";
            if(phoneVal && !/^\\d{10}$/.test(phoneVal)) {
                alert("Mobile number must be exactly 10 digits.");
                document.getElementById("contact").classList.add("ap-invalid");
                valid = false;
            }

            // File inputs
            const fileInputs = ['photoUpload', 'employeeSignature', 'applicantSignature', 'medicalDocument'];
            const files = {};
            
            fileInputs.forEach(id => {
                const fileEl = document.getElementById(id);
                if (fileEl && fileEl.files[0]) {
                    files[id] = fileEl.files[0];
                } else if (fileEl && fileEl.hasAttribute('data-required')) {
                    alert("Please upload the required file for: " + id);
                    valid = false;
                }
            });
            
            if(!valid) {
                alert("Please fill all required fields correctly.");
                return;
            }

            submitBtn.innerText = "Processing & Validating... Please wait";
            submitBtn.disabled = true;

            try {
                if(!supabase) throw new Error("Supabase is not connected.");
                
                // Check uniqueness in DB
                const { data: existingData, error: fetchErr } = await supabase
                    .from('applications')
                    .select('id')
                    .or(`contact.eq.${phoneVal},email.eq.${emailVal}`);
                
                if(fetchErr) throw fetchErr;
                if(existingData && existingData.length > 0) {
                    throw new Error("Duplicate entry: An application with this mobile number or email already exists.");
                }

                submitBtn.innerText = "Uploading Files... Please wait";

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

                submitBtn.innerText = "Finalizing Application...";

                // Insert DB
                const { error: dbErr } = await supabase.from('applications').insert([{
                    participant_name: data.participantName,
                    employee_name: data.employeeName,
                    contact: phoneVal,
                    email: emailVal,
                    form_image_url: urls.photoUpload, // Use photo as primary image
                    raw_data: { ...data, urls }
                }]);
                
                if(dbErr) throw dbErr;
                
                successPopup.classList.add("show");
            } catch(e) {
                console.error(e);
                alert("Error: " + e.message);
            } finally {
                submitBtn.innerText = "Submit Application";
                submitBtn.disabled = false;
            }
        });
    }

    if(closePopupBtn) {
        closePopupBtn.addEventListener("click", () => {
            successPopup.classList.remove("show");
            location.reload();
        });
    }
});
"""

with open("app_v6.js", "w", encoding="utf-8") as f:
    f.write(js)
