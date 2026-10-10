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
        modal.classList.remove("show");
    });

    window.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.classList.remove("show");
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
        const titleEl = document.getElementById('modalTitle');
        if(titleEl) titleEl.innerText = `Application Details: ${row.participant_name || 'N/A'}`;
        
        let rawData = {};
        if (row.raw_data) {
            try {
                rawData = typeof row.raw_data === 'string' ? JSON.parse(row.raw_data) : row.raw_data;
            } catch(e) {}
        }
        
        const md = document.getElementById('modalData');
        let html = '';
        
        const addRow = (label, val) => {
            html += `<div class="data-row"><div class="data-label">${label}</div><div class="data-value">${val || '<em>N/A</em>'}</div></div>`;
        };
        
        addRow("Database ID", row.id);
        addRow("Submitted At", new Date(row.created_at).toLocaleString());
        
        if (rawData) {
            const keys = Object.keys(rawData).filter(k => k !== 'urls' && k !== 'submitted_at');
            keys.forEach(k => {
                const label = k.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase());
                addRow(label, rawData[k]);
            });
            
            if (rawData.urls && rawData.urls.filledFormDocument) {
                html += `<div class="data-row" style="margin-top: 15px;">
                            <div class="data-label" style="color:var(--navy);">Attached Document</div>
                            <div class="data-value">
                                <a href="${rawData.urls.filledFormDocument}" target="_blank" class="btn btn-outline" style="padding: 6px 12px; font-size: 14px;">
                                    View PDF Document
                                </a>
                            </div>
                         </div>`;
            }
        }
        
        md.innerHTML = html;
        modal.classList.add("show");
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
