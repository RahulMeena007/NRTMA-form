document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("formCanvas");
    const ctx = canvas.getContext("2d");
    const bgImage = document.getElementById("bg-image");
    const form = document.getElementById("nrtma-form");
    const downloadBtn = document.getElementById("downloadBtn");
    const statusMsg = document.getElementById("status-message");

    // Supabase configuration (Replace with your actual keys)
    const SUPABASE_URL = 'https://dlqsexaiunsploctiwza.supabase.co';
    const SUPABASE_ANON_KEY = 'sb_publishable_x5Zm3FXPFNH7tZcq5S3FmA_olJJS5LT';
    // Initialize Supabase client
    const supabase = window.supabase ? window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY) : null;

    let userPhotoImg = null;

    // Load background and initial draw
    bgImage.onload = () => {
        drawCanvas();
    };

    // If image is already loaded from cache
    if (bgImage.complete) {
        drawCanvas();
    }

    // Input fields mapping to coordinates [x, y]
    const textCoords = {
        trekName: [250, 185],
        participantName: [210, 215],
        employeeName: [170, 245],
        relation: [210, 273],
        designation: [210, 292],
        officeAddress: [150, 310],
        dob: [180, 328],
        doa: [460, 328],
        contact: [150, 345],
        email: [410, 345],
        residentialAddress: [180, 362],
        experience: [480, 375],
        
        illness: [250, 646],
        injuries: [320, 661],
        allergy: [260, 676],
        bloodGroup: [150, 690],
        
        infectious: [460, 706],
        skin: [460, 720],
        heart: [460, 735],
        asthmatic: [460, 750],
        otherDisease: [460, 765]
    };

    // Listen to all inputs to re-draw canvas live
    const inputs = form.querySelectorAll('input:not([type="file"]), select');
    inputs.forEach(input => {
        input.addEventListener('input', drawCanvas);
    });

    // Handle photo upload for preview
    const photoInput = document.getElementById('photoUpload');
    photoInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                const img = new Image();
                img.onload = () => {
                    userPhotoImg = img;
                    drawCanvas();
                };
                img.src = event.target.result;
            };
            reader.readAsDataURL(file);
        } else {
            userPhotoImg = null;
            drawCanvas();
        }
    });

    function drawCanvas() {
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw background
        ctx.drawImage(bgImage, 0, 0, canvas.width, canvas.height);

        // Draw User Photo if uploaded
        if (userPhotoImg) {
            // Photo box coordinates based on the image: x, y, width, height
            const photoX = 508;
            const photoY = 155;
            const photoW = 100;
            const photoH = 120;
            
            // Draw photo covering the box
            ctx.drawImage(userPhotoImg, photoX, photoY, photoW, photoH);
        }

        // Setup font styles for cursive handwriting
        // Using Caveat font loaded in HTML
        ctx.font = "22px 'Caveat', cursive";
        ctx.fillStyle = "#1e3a8a"; // Dark blue ink color

        // Iterate through inputs and draw text
        inputs.forEach(input => {
            const id = input.id;
            const val = input.value;
            
            if (val && textCoords[id]) {
                const [x, y] = textCoords[id];
                ctx.fillText(val, x, y);
            }
        });
    }

    // Form Submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        statusMsg.textContent = "Processing & Saving...";
        statusMsg.className = "status";
        
        // Final draw to ensure accuracy
        drawCanvas();
        
        // Get the final image data
        const finalImageDataUrl = canvas.toDataURL('image/jpeg', 0.9);
        
        try {
            // --- SUPABASE INTEGRATION LOGIC ---
            // In a real scenario with proper keys, this block will execute:
            if (SUPABASE_URL !== 'https://your-project-id.supabase.co') {
                
                // 1. Convert DataURL to Blob for storage upload
                const res = await fetch(finalImageDataUrl);
                const blob = await res.blob();
                
                const fileName = `form_${Date.now()}.jpg`;
                
                // 2. Upload final image to Supabase Storage ('nrtma-forms' bucket)
                const { data: uploadData, error: uploadError } = await supabase
                    .storage
                    .from('nrtma-forms')
                    .upload(`filled/${fileName}`, blob);
                    
                if (uploadError) throw uploadError;
                
                // 3. Get public URL of the uploaded image
                const { data: publicUrlData } = supabase
                    .storage
                    .from('nrtma-forms')
                    .getPublicUrl(`filled/${fileName}`);
                
                // 4. Save form details to Supabase Database ('applications' table)
                const formData = {};
                inputs.forEach(input => formData[input.id] = input.value);
                
                const { data: dbData, error: dbError } = await supabase
                    .from('applications')
                    .insert([
                        { 
                            participant_name: formData.participantName,
                            employee_name: formData.employeeName,
                            contact: formData.contact,
                            form_image_url: publicUrlData.publicUrl,
                            raw_data: formData 
                        }
                    ]);
                    
                if (dbError) throw dbError;
            } else {
                // Simulation for demo purposes
                await new Promise(resolve => setTimeout(resolve, 1500));
                console.log("Mock saved to Supabase!");
            }
            
            statusMsg.textContent = "Successfully Generated and Saved!";
            statusMsg.className = "status success";
            
            // Enable download button
            downloadBtn.disabled = false;
            
            // Attach download functionality
            downloadBtn.onclick = () => {
                const link = document.createElement('a');
                link.download = `NRTMA_Application_${document.getElementById('participantName').value || 'Form'}.jpg`;
                link.href = finalImageDataUrl;
                link.click();
            };

        } catch (error) {
            console.error(error);
            statusMsg.textContent = "Error saving to database. Please check your Supabase configuration.";
            statusMsg.className = "status error";
        }
    });
});
