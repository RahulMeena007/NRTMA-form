document.addEventListener("DOMContentLoaded", () => {
    // Supabase configuration
    const SUPABASE_URL = 'https://dlqsexaiunsploctiwza.supabase.co';
    const SUPABASE_ANON_KEY = 'sb_publishable_x5Zm3FXPFNH7tZcq5S3FmA_olJJS5LT';
    const supabase = window.supabase ? window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY) : null;

    // Elements
    const formSection = document.getElementById("form-section");
    const previewSection = document.getElementById("preview-section");
    const previewBtn = document.getElementById("previewBtn");
    const editBtn = document.getElementById("editBtn");
    const submitUploadBtn = document.getElementById("submitUploadBtn");
    const successPopup = document.getElementById("successPopup");
    const closePopupBtn = document.getElementById("closePopupBtn");
    const canvas = document.getElementById("formCanvas");
    const ctx = canvas.getContext("2d");
    const bgImage = document.getElementById("bg-image");
    
    let userPhotoImg = null;
    let rawPhotoFile = null;

    const textCoords = {
        trekName: [360, 153],
        participantName: [300, 193],
        employeeName: [280, 227],
        relation: [320, 253],
        designation: [280, 278],
        officeAddress: [220, 298],
        dob: [260, 318],
        doa: [460, 318],
        contact: [220, 338],
        email: [480, 338],
        residentialAddress: [260, 358],
        experience: [480, 378],
        illness: [320, 635],
        injuries: [390, 650],
        allergy: [350, 665],
        bloodGroup: [240, 680],
        infectious: [380, 695],
        skin: [380, 710],
        heart: [380, 725],
        asthmatic: [380, 740],
        otherDisease: [380, 755]
    };

    const inputs = document.querySelectorAll('input:not([type="file"]), select');
    const photoInput = document.getElementById('photoUpload');

    photoInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            rawPhotoFile = file;
            const reader = new FileReader();
            reader.onload = (event) => {
                const img = new Image();
                img.onload = () => { userPhotoImg = img; };
                img.src = event.target.result;
            };
            reader.readAsDataURL(file);
        } else {
            userPhotoImg = null;
            rawPhotoFile = null;
        }
    });

    // Custom Async Validation
    async function validateForm() {
        let isValid = true;
        let firstInvalidField = null;
        
        // Clear old errors
        document.querySelectorAll('.input-error').forEach(el => el.classList.remove('input-error'));
        document.querySelectorAll('.field-error-msg').forEach(el => el.remove());

        function showError(field, msg) {
            isValid = false;
            field.classList.add('input-error');
            const errorEl = document.createElement('div');
            errorEl.className = 'field-error-msg';
            errorEl.style.display = 'block';
            errorEl.innerText = msg;
            field.parentElement.appendChild(errorEl);
            
            if (!firstInvalidField) firstInvalidField = field;
        }

        const reqFields = document.querySelectorAll('[data-required="true"]');
        for (const field of reqFields) {
            if (field.type === 'file') {
                if (!rawPhotoFile) {
                    showError(field, "Please upload a passport size photo.");
                }
            } else {
                const val = field.value.trim();
                if (val === '') {
                    showError(field, "This field cannot be empty.");
                } else if (field.pattern) {
                    const regex = new RegExp('^' + field.pattern + '$');
                    if (!regex.test(val)) {
                        showError(field, field.title || "Invalid format.");
                    }
                }
            }
        }

        // Check for duplicates in Supabase if contact is valid so far
        const contactField = document.getElementById("contact");
        if (isValid && supabase && contactField.value.trim() !== '') {
            try {
                const { data } = await supabase
                    .from('applications')
                    .select('id')
                    .eq('contact', contactField.value.trim());
                    
                if (data && data.length > 0) {
                    showError(contactField, "An application with this phone number already exists!");
                }
            } catch (err) {
                console.warn("Could not check duplicate", err);
            }
        }

        if (!isValid && firstInvalidField) {
            firstInvalidField.scrollIntoView({ behavior: 'smooth', block: 'center' });
            firstInvalidField.focus();
        }
        
        return isValid;
    }

    function drawCanvas() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(bgImage, 0, 0, canvas.width, canvas.height);

        if (userPhotoImg) {
            const photoX = 508, photoY = 155, photoW = 100, photoH = 120;
            ctx.drawImage(userPhotoImg, photoX, photoY, photoW, photoH);
        }

        ctx.font = "16px 'Caveat', cursive";
        ctx.fillStyle = "#1e3a8a"; // Blue ink

        inputs.forEach(input => {
            const id = input.id;
            const val = input.value;
            if (val && textCoords[id]) {
                const [x, y] = textCoords[id];
                ctx.fillText(val, x, y);
            }
        });
    }

    // --- BUTTON ACTIONS ---

    previewBtn.addEventListener("click", async () => {
        if (!navigator.onLine) {
            alert("You are currently offline. Please connect to the internet.");
            return;
        }

        previewBtn.innerText = "Checking & Validating...";
        previewBtn.disabled = true;

        const valid = await validateForm();
        
        previewBtn.innerText = "Review Form";
        previewBtn.disabled = false;

        if (valid) {
            drawCanvas();
            formSection.classList.add("hidden");
            previewSection.classList.remove("hidden");
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });

    editBtn.addEventListener("click", () => {
        previewSection.classList.add("hidden");
        formSection.classList.remove("hidden");
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    submitUploadBtn.addEventListener("click", async () => {
        if(!supabase) {
            alert("Supabase client is not initialized.");
            return;
        }

        const originalText = submitUploadBtn.innerText;
        submitUploadBtn.innerText = "Uploading... Please Wait";
        submitUploadBtn.disabled = true;
        editBtn.disabled = true;

        try {
            const timestamp = Date.now();
            
            // 1. Upload original photo
            let uploadedPhotoUrl = null;
            if (rawPhotoFile) {
                const ext = rawPhotoFile.name.split('.').pop() || 'jpg';
                const photoName = `user_${timestamp}.${ext}`;
                const { error: photoErr } = await supabase.storage
                    .from('nrtma-forms')
                    .upload(`photos/${photoName}`, rawPhotoFile);
                if (photoErr) throw photoErr;
                
                const { data: pUrlData } = supabase.storage
                    .from('nrtma-forms')
                    .getPublicUrl(`photos/${photoName}`);
                uploadedPhotoUrl = pUrlData.publicUrl;
            }

            // 2. Upload generated form image
            const finalImageDataUrl = canvas.toDataURL('image/jpeg', 0.9);
            const res = await fetch(finalImageDataUrl);
            const blob = await res.blob();
            const formName = `form_${timestamp}.jpg`;
            
            const { error: formErr } = await supabase.storage
                .from('nrtma-forms')
                .upload(`filled/${formName}`, blob);
            if (formErr) throw formErr;
            
            const { data: fUrlData } = supabase.storage
                .from('nrtma-forms')
                .getPublicUrl(`filled/${formName}`);
            
            // 3. Save to database
            const formData = {};
            inputs.forEach(i => formData[i.id] = i.value);
            if (uploadedPhotoUrl) {
                formData.photo_url = uploadedPhotoUrl;
            }
            formData.submitted_at = new Date().toISOString();
            
            const { error: dbErr } = await supabase
                .from('applications')
                .insert([{ 
                    participant_name: formData.participantName,
                    employee_name: formData.employeeName,
                    contact: formData.contact,
                    form_image_url: fUrlData.publicUrl,
                    raw_data: formData 
                }]);
                
            if (dbErr) throw dbErr;

            // Success!
            successPopup.style.display = "flex";

        } catch (error) {
            console.error(error);
            alert("Failed to upload: " + error.message);
        } finally {
            submitUploadBtn.innerText = originalText;
            submitUploadBtn.disabled = false;
            editBtn.disabled = false;
        }
    });

    closePopupBtn.addEventListener("click", () => {
        successPopup.style.display = "none";
        document.getElementById("nrtma-form").reset();
        userPhotoImg = null;
        rawPhotoFile = null;
        previewSection.classList.add("hidden");
        formSection.classList.remove("hidden");
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});
