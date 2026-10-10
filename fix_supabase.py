with open("app_v6.js", "r", encoding="utf-8") as f:
    js = f.read()

supabase_init = """
const SUPABASE_URL = 'https://dlqsexaiunsploctiwza.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_x5Zm3FXPFNH7tZcq5S3FmA_olJJS5LT';
const supabase = window.supabase ? window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY) : null;

"""

if "const supabase =" not in js:
    js = supabase_init + js
    with open("app_v6.js", "w", encoding="utf-8") as f:
        f.write(js)
    print("Added supabase init")
else:
    print("Supabase init already present")
