document.addEventListener("DOMContentLoaded", () => {
    // Supabase configuration
    const SUPABASE_URL = 'https://dlqsexaiunsploctiwza.supabase.co';
    const SUPABASE_ANON_KEY = 'sb_publishable_x5Zm3FXPFNH7tZcq5S3FmA_olJJS5LT';
    const supabase = window.supabase ? window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY) : null;

    // UI Elements
    const loginContainer = document.getElementById("login-container");
    const dashboardContainer = document.getElementById("dashboard-container");
    const loginBtn = document.getElementById("loginBtn");
    const logoutBtn = document.getElementById("logoutBtn");
    const loginError = document.getElementById("loginError");
    const userInp = document.getElementById("adminUsername");
    const passInp = document.getElementById("adminPassword");
    const submissionsTable = document.getElementById("submissionsTable");
    
    const modal = document.getElementById("detailsModal");
    const closeModal = document.getElementById("closeModal");
    const modalData = document.getElementById("modalData");

    // Hardcoded credentials as requested
    const ADMIN_USER = "777RM07";
    const ADMIN_PASS = "Rahul7850";

    // Check if already logged in via sessionStorage
    if (sessionStorage.getItem("adminLoggedIn") === "true") {
        showDashboard();
    }

    loginBtn.addEventListener("click", () => {
        if (userInp.value === ADMIN_USER && passInp.value === ADMIN_PASS) {
            sessionStorage.setItem("adminLoggedIn", "true");
            showDashboard();
        } else {
            loginError.style.display = "block";
        }
    });

    logoutBtn.addEventListener("click", () => {
        sessionStorage.removeItem("adminLoggedIn");
        dashboardContainer.style.display = "none";
        loginContainer.style.display = "block";
        userInp.value = "";
        passInp.value = "";
        loginError.style.display = "none";
    });

    closeModal.addEventListener("click", () => {
        modal.style.display = "none";
    });

    window.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });

    async function showDashboard() {
        loginContainer.style.display = "none";
        dashboardContainer.style.display = "block";
        await fetchSubmissions();
        await fetchQueries();
    }

    async function fetchSubmissions() {
        if (!supabase) {
            submissionsTable.innerHTML = "<tr><td colspan='5' style='color:red;'>Supabase client not loaded.</td></tr>";
            return;
        }

        try {
            // Removed order clause completely since table is missing id and created_at
            const { data, error } = await supabase
                .from('applications')
                .select('*');

            if (error) throw error;

            if (!data || data.length === 0) {
                submissionsTable.innerHTML = "<tr><td colspan='5' style='text-align:center;'>No submissions found yet.</td></tr>";
                return;
            }

            submissionsTable.innerHTML = "";

            data.forEach(row => {
                const tr = document.createElement("tr");
                
                // Extract photo URL and timestamp if they exist
                let rawData = {};
                try {
                    rawData = typeof row.raw_data === 'string' ? JSON.parse(row.raw_data) : row.raw_data;
                } catch(e) {}
                
                // Format date nicely as DD/MM/YYYY + Time
                const timestampToUse = (rawData && rawData.submitted_at) ? rawData.submitted_at : row.created_at;
                const dateObj = new Date(timestampToUse);
                let dateStr = "Unknown Time";
                if (!isNaN(dateObj)) {
                    const dd = String(dateObj.getDate()).padStart(2, '0');
                    const mm = String(dateObj.getMonth() + 1).padStart(2, '0');
                    const yyyy = dateObj.getFullYear();
                    const time = dateObj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }); 
                    dateStr = `${dd}/${mm}/${yyyy} <br><span style="font-size:0.85rem;color:#6b7280">${time}</span>`;
                }

                

                tr.innerHTML = `
                    <td>${dateStr}</td>
                    
                    <td><strong>${row.participant_name || 'N/A'}</strong></td>
                    <td>${row.employee_name || 'N/A'}</td>

                    <td>
                        <div style="display:flex; flex-direction:column; gap:5px; font-size:0.9rem;">
                        ${(rawData && rawData.urls && rawData.urls.filledFormDocument) ? `<a href="${rawData.urls.filledFormDocument}" target="_blank" style="color:#10b981; font-weight:600;">View Filled Form PDF</a>` : '<span style="color:var(--muted)">No PDF Uploaded</span>'}
                        </div>
                    </td>

                    <td>
                        <button class="details-btn">View All Typed Data</button>
                    </td>
                `;

                // Add event listener to the details button
                const btn = tr.querySelector('.details-btn');
                btn.addEventListener('click', () => {
                    openDetailsModal(row);
                });

                submissionsTable.appendChild(tr);
            });

        } catch (error) {
            console.error("Error fetching data:", error);
            submissionsTable.innerHTML = `<tr><td colspan='5' style='color:red; text-align:center;'>Failed to load data: ${error.message}</td></tr>`;
        }
    }

    function openDetailsModal(row) {
        let html = `
            <p><strong>Database ID:</strong> ${row.id}</p>
            <p><strong>Submitted At:</strong> ${new Date(row.created_at).toLocaleString()}</p>
            <p><strong>Participant Name:</strong> ${row.participant_name}</p>
            <p><strong>Employee Name:</strong> ${row.employee_name}</p>
            <p><strong>Contact:</strong> ${row.contact}</p>
            <hr style="margin: 15px 0; border: 0; border-top: 1px solid #ccc;">
            <h4 style="margin-bottom: 10px;">Raw Form Entries (JSON)</h4>
        `;
        
        // Loop through the raw_data JSON object
        if (row.raw_data) {
            html += `<table style="width:100%; border:1px solid #eee;">`;
            for (const [key, value] of Object.entries(row.raw_data)) {
                html += `<tr>
                            <td style="background:#f9fafb; font-weight:600; width:40%;">${key}</td>
                            <td>${value || '<em>blank</em>'}</td>
                         </tr>`;
            }
            html += `</table>`;
        } else {
            html += `<p>No extra raw data saved.</p>`;
        }

        modalData.innerHTML = html;
        modal.style.display = "flex";
    }

    async function fetchQueries() {
        const queriesTable = document.getElementById("queriesTable");
        if (!supabase || !queriesTable) return;

        try {
            const { data, error } = await supabase
                .from('queries')
                .select('*');

            if (error) throw error;

            if (!data || data.length === 0) {
                queriesTable.innerHTML = "<tr><td colspan='4' style='text-align:center;'>No queries found.</td></tr>";
                return;
            }

            // Sort queries manually if they have created_at
            data.sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0));

            queriesTable.innerHTML = "";
            data.forEach(q => {
                const tr = document.createElement("tr");
                
                const dateObj = new Date(q.created_at);
                let dateStr = "Unknown Date";
                if (!isNaN(dateObj)) {
                    dateStr = dateObj.toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });
                }

                tr.innerHTML = `
                    <td>${dateStr}</td>
                    <td><strong>${q.name || 'N/A'}</strong></td>
                    <td><a href="mailto:${q.email}">${q.email || 'N/A'}</a></td>
                    <td>${q.contact || 'N/A'}</td>
                `;
                queriesTable.appendChild(tr);
            });
        } catch (err) {
            console.error("Query fetch error", err);
            queriesTable.innerHTML = `<tr><td colspan="4" style="color:red; text-align:center;">Failed to load queries. (Did you create the queries table in Supabase?)</td></tr>`;
        }
    }
});
