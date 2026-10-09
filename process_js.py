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
            
            if(!valid) {
                alert("Please fill all required fields.");
                return;
            }

            submitBtn.innerText = "Processing... Please wait";
            submitBtn.disabled = true;

            try {
                if(typeof supabase !== 'undefined') {
                    // Check DB
                    const { error: dbErr } = await supabase.from('applications').insert([{
                        participant_name: data.participantName,
                        employee_name: data.employeeName,
                        contact: data.contact,
                        email: data.email,
                        raw_data: data
                    }]);
                    if(dbErr) throw dbErr;
                }
                
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
