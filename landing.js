document.addEventListener('DOMContentLoaded', () => {
    // Supabase config
    const SUPABASE_URL = 'https://dlqsexaiunsploctiwza.supabase.co';
    const SUPABASE_ANON_KEY = 'sb_publishable_x5Zm3FXPFNH7tZcq5S3FmA_olJJS5LT';
    const supabase = window.supabase ? window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY) : null;

    // Countdown Timers
    function adjustActiveGrid() {
        const activeGrid = document.querySelector('.camps-grid');
        if (!activeGrid) return;
        const activeCards = activeGrid.querySelectorAll('.camp-card');
        if (activeCards.length === 1) {
            activeGrid.classList.add('centered');
        } else {
            activeGrid.classList.remove('centered');
        }
    }

    function convertToExpired(card) {
        const expiredGrid = document.querySelector('.expired-camps-grid');
        if (!expiredGrid) return;
        
        // Extract info
        const img = card.querySelector('img');
        const imgSrc = img ? img.src : '';
        const imgAlt = img ? img.alt : '';
        
        const campTagEl = card.querySelector('.camp-tag');
        const campTag = campTagEl ? campTagEl.innerText : 'Camp';
        
        const h3El = card.querySelector('h3');
        const title = h3El ? h3El.innerText : '';
        
        const locEl = card.querySelector('.camp-loc');
        const locHtml = locEl ? locEl.innerHTML : '';
        
        // Extract dates and price
        const metaRows = card.querySelectorAll('.meta-row');
        let dates = "";
        let price = "";
        metaRows.forEach(row => {
            if(row.innerText.includes('Dates')) {
                const spans = row.querySelectorAll('span');
                if (spans.length > 1) dates = spans[1].innerText;
            }
            if(row.innerText.includes('Fee')) {
                const priceEl = row.querySelector('.camp-price');
                if (priceEl) price = priceEl.innerText;
            }
        });

        // Build expired card HTML
        const expiredHtml = `
            <div class="camp-img-wrap">
                <img src="${imgSrc}" alt="${imgAlt}">
                <div class="expired-tag">EXPIRED</div>
                <span class="camp-tag tag-theme">${campTag}</span>
            </div>
            <div class="camp-body">
                <p class="camp-loc">${locHtml}</p>
                <h3>${title}</h3>
                <div class="camp-meta">
                    <div class="meta-row"><span class="meta-icon">📅</span><span>${dates}</span></div>
                    <div class="meta-row price-col"><span class="meta-label">FROM</span><span class="price-val">${price}</span></div>
                </div>
            </div>
        `;

        // change class and inject
        card.className = "camp-card expired-card theme-red"; 
        card.innerHTML = expiredHtml;

        // move to expired grid
        expiredGrid.insertBefore(card, expiredGrid.firstChild);

        // check active grid
        adjustActiveGrid();
    }

    function updateCountdowns() {
        const timers = document.querySelectorAll('.countdown');
        const now = new Date().getTime();

        timers.forEach(timer => {
            const targetDateStr = timer.getAttribute('data-date');
            if (!targetDateStr) return;
            const target = new Date(targetDateStr).getTime();
            const distance = target - now;

            if (distance < 0) {
                if (!timer.closest('.expired-card')) {
                    const campCard = timer.closest('.camp-card');
                    if (campCard) {
                        convertToExpired(campCard);
                    }
                }
                return;
            }

            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            timer.innerHTML = `⏱ Closes in: ${days}d ${hours}h ${minutes}m ${seconds}s`;
        });
    }
    
    // Initial adjust on load
    adjustActiveGrid();
    
    updateCountdowns();
    setInterval(updateCountdowns, 1000);

    // Modals
    const applyModal = document.getElementById('applyModal');
    const queryModal = document.getElementById('queryModal');
    
    // Buttons
    const applyBtns = document.querySelectorAll('.apply-trigger');
    const closeApplyBtn = document.querySelector('.close-modal');
    const closeQueryBtn = document.getElementById('closeQueryBtn');
    
    // Apply Modal Logic
    applyBtns.forEach(btn => {
        btn.addEventListener('click', () => applyModal.classList.remove('hidden'));
    });
    closeApplyBtn.addEventListener('click', () => applyModal.classList.add('hidden'));
    applyModal.addEventListener('click', (e) => {
        if (e.target === applyModal) applyModal.classList.add('hidden');
    });

    // 8-second Query Popup Logic
    let queryShown = false;
    setTimeout(() => {
        // Only show if the apply modal isn't currently open
        if (!queryShown && applyModal.classList.contains('hidden')) {
            queryModal.classList.remove('hidden');
            queryShown = true;
        }
    }, 8000);

    closeQueryBtn.addEventListener('click', () => queryModal.classList.add('hidden'));
    queryModal.addEventListener('click', (e) => {
        if (e.target === queryModal) queryModal.classList.add('hidden');
    });

    // Query Form Submission
    const queryForm = document.getElementById('queryForm');
    const querySuccess = document.getElementById('querySuccess');
    const querySubmitBtn = queryForm.querySelector('button[type="submit"]');

    queryForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (!supabase) {
            alert("Database connection not available.");
            return;
        }

        const name = document.getElementById('qName').value;
        const email = document.getElementById('qEmail').value;
        const contact = document.getElementById('qContact').value;

        querySubmitBtn.innerText = "Sending...";
        querySubmitBtn.disabled = true;

        try {
            const { error } = await supabase
                .from('queries')
                .insert([{ name, email, contact }]);
            
            if (error) throw error;

            // Success
            queryForm.style.display = 'none';
            querySuccess.classList.remove('hidden');
            
            setTimeout(() => {
                queryModal.classList.add('hidden');
            }, 3000);

        } catch (err) {
            alert("Error sending query: " + err.message);
            querySubmitBtn.innerText = "Send Query";
            querySubmitBtn.disabled = false;
        }
    });

    // Fade-in Animation Observer
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    };
    
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.fade-in').forEach(el => {
        observer.observe(el);
    });
});
