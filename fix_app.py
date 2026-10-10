js_content = """
const SUPABASE_URL = 'https://dlqsexaiunsploctiwza.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_x5Zm3FXPFNH7tZcq5S3FmA_olJJS5LT';
const supabase = window.supabase ? window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY) : null;

document.addEventListener("DOMContentLoaded", () => {
    const btnOption1 = document.getElementById("btnOption1");
    const choiceSection = document.getElementById("choice-section");
    const formSection = document.getElementById("form-section");
    const onlineBackBtn = document.getElementById("onlineBackBtn");
    const onlineBackBtnBottom = document.getElementById("onlineBackBtnBottom");
    const submitBtn = document.getElementById("submitBtn");
    const successPopup = document.getElementById("successPopup");
    const closePopupBtn = document.getElementById("closePopupBtn");

    if (btnOption1) {
        btnOption1.addEventListener("click", () => { 
            if(choiceSection) choiceSection.classList.add("hidden"); 
            if(formSection) formSection.classList.remove("hidden"); 
        });
    }
    
    if (onlineBackBtn) {
        onlineBackBtn.addEventListener("click", () => { 
            if(formSection) formSection.classList.add("hidden"); 
            if(choiceSection) choiceSection.classList.remove("hidden"); 
        });
    }
    
    if (onlineBackBtnBottom) {
        onlineBackBtnBottom.addEventListener("click", () => { 
            if(formSection) formSection.classList.add("hidden"); 
            if(choiceSection) choiceSection.classList.remove("hidden"); 
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

            const emailVal = data.email || "";
            if(emailVal && !emailVal.endsWith("@gmail.com")) {
                alert("Email must be a @gmail.com address.");
                document.getElementById("email").classList.add("ap-invalid");
                valid = false;
            }
            
            const phoneVal = data.contact || "";
            if(phoneVal && !/^\d{10}$/.test(phoneVal)) {
                alert("Mobile number must be exactly 10 digits.");
                document.getElementById("contact").classList.add("ap-invalid");
                valid = false;
            }

            const fileInputs = ['filledFormDocument'];
            const files = {};
            
            fileInputs.forEach(id => {
                const fileEl = document.getElementById(id);
                if (fileEl && fileEl.files[0]) {
                    if (fileEl.files[0].size > 4 * 1024 * 1024) {
                        alert("File size for " + id + " exceeds 4 MB. Please upload a smaller PDF.");
                        valid = false;
                    } else {
                        files[id] = fileEl.files[0];
                    }
                } else if (fileEl && fileEl.hasAttribute('data-required')) {
                    alert("Please upload the filled application form PDF.");
                    valid = false;
                }
            });
            
            if(!valid) {
                alert("Please fill all required fields and upload the PDF.");
                return;
            }

            submitBtn.innerText = "Processing & Validating... Please wait";
            submitBtn.disabled = true;

            try {
                if(!supabase) throw new Error("Supabase is not connected.");
                
                const { data: existingData, error: fetchErr } = await supabase
                    .from('applications')
                    .select('id')
                    .or(`contact.eq.${phoneVal},email.eq.${emailVal}`);
                
                if(fetchErr) throw fetchErr;
                if(existingData && existingData.length > 0) {
                    throw new Error("Duplicate entry: An application with this mobile number or email already exists.");
                }

                submitBtn.innerText = "Uploading PDF... Please wait";

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

                const { error: dbErr } = await supabase.from('applications').insert([{
                    participant_name: data.participantName,
                    employee_name: data.employeeName,
                    contact: phoneVal,
                    email: emailVal,
                    form_image_url: urls.filledFormDocument,
                    raw_data: { ...data, urls }
                }]);
                
                if(dbErr) throw dbErr;
                
                if(successPopup) successPopup.classList.add("show");
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
            if(successPopup) successPopup.classList.remove("show");
            location.reload();
        });
    }
});
"""
with open("app_v6.js", "w", encoding="utf-8") as f:
    f.write(js_content)
