with open("app_v6.js", "r", encoding="utf-8") as f:
    js = f.read()

# Remove the global supabase init
js = js.replace("""const SUPABASE_URL = 'https://dlqsexaiunsploctiwza.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_x5Zm3FXPFNH7tZcq5S3FmA_olJJS5LT';
const supabase = window.supabase ? window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY) : null;""", "")

# Insert it inside DOMContentLoaded
js = js.replace('document.addEventListener("DOMContentLoaded", () => {', """document.addEventListener("DOMContentLoaded", () => {
    const SUPABASE_URL = 'https://dlqsexaiunsploctiwza.supabase.co';
    const SUPABASE_ANON_KEY = 'sb_publishable_x5Zm3FXPFNH7tZcq5S3FmA_olJJS5LT';
    const supabase = window.supabase ? window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY) : null;
""")

with open("app_v6.js", "w", encoding="utf-8") as f:
    f.write(js)
