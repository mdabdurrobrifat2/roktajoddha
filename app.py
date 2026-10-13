from flask import Flask, request, redirect, render_template_string
import sqlite3, os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('roktajoddha.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS donors
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT, blood TEXT, phone TEXT, country TEXT, city TEXT)''')
    conn.commit(); conn.close()
init_db()

PAGE = """
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ROKTO JODDHA - Global Blood Network</title>
<style>
*{box-sizing:border-box}body{margin:0;font-family:sans-serif;background:#fff5f5}
.header{background:#b91c1c;color:white;padding:25px;text-align:center}
.header h1{margin:0;font-size:36px}
.container{max-width:1000px;margin:auto;padding:15px}
.card{background:white;border-radius:15px;padding:15px;box-shadow:0 4px 15px rgba(0,0,0,.07);margin-bottom:12px}
.badge{background:#b91c1c;color:white;padding:5px 14px;border-radius:20px;font-weight:bold}
input,select{width:100%;padding:13px;border-radius:10px;border:1px solid #ddd;margin-bottom:10px}
.btn{width:100%;padding:13px;border-radius:10px;border:none;font-weight:bold;cursor:pointer}
.btn-red{background:#b91c1c;color:white}
.btn-green{background:#16a34a;color:white}
</style></head><body>
<div class="header">
<h1>🩸 ROKTO JODDHA</h1>
<p>BLOOD DONOR NETWORK | দেশ-বিদেশের রক্তযোদ্ধা</p>
<p>🌍 Bangladesh | Saudi | Malaysia | USA | UK | UAE | সারা বিশ্ব</p>
</div>
<div class="container">
<div class="card">
<form method="GET" style="display:grid;grid-template-columns:1fr 1fr auto;gap:8px">
<select name="blood"><option value="">সব ব্লাড গ্রুপ</option><option>A+</option><option>A-</option><option>B+</option><option>B-</option><option>O+</option><option>O-</option><option>AB+</option><option>AB-</option></select>
<input name="city" placeholder="শহর / দেশ লিখুন" value="{{city}}">
<button class="btn btn-red">Search</button>
</form>
</div>

{% for d in donors %}
<div class="card" style="border-left:6px solid #b91c1c;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap">
<div>
<b style="font-size:18px">{{d[1]}}</b> <span class="badge">{{d[2]}}</span><br>
<small style="color:#666">📍 {{d[5]}}, {{d[4]}} | 📞 {{d[3]}}</small>
</div>
<div style="display:flex;gap:8px;margin-top:8px">
<a href="tel:{{d[3]}}" style="background:#b91c1c;color:white;padding:10px 14px;border-radius:8px;text-decoration:none">📞 কল</a>
<a href="https://wa.me/88{{d[3]}}" target="_blank" style="background:#25D366;color:white;padding:10px 14px;border-radius:8px;text-decoration:none">WhatsApp</a>
</div>
</div>
{% endfor %}

<div class="card" style="background:#0a192f;color:white">
<h3 style="margin-top:0;color:#00FF88">➕ রক্তযোদ্ধা হিসাবে যোগ দিন - Join as Warrior</h3>
<form method="POST">
<input name="name" placeholder="আপনার নাম *" required>
<select name="blood" required><option value="">ব্লাড গ্রুপ *</option><option>A+</option><option>A-</option><option>B+</option><option>B-</option><option>O+</option><option>O-</option><option>AB+</option><option>AB-</option></select>
<input name="phone" placeholder="মোবাইল / WhatsApp *" required>
<select name="country" required><option>Bangladesh</option><option>Saudi Arabia</option><option>Malaysia</option><option>USA</option><option>UK</option><option>UAE</option><option>India</option><option>Other</option></select>
<input name="city" placeholder="শহর / জেলা *" required>
<button class="btn" style="background:#00FF88;color:black">আমি রক্ত দিতে প্রস্তুত</button>
</form>
</div>

<p style="text-align:center;color:#999;margin-top:30px">ROKTO JODDHA v1.0 | এক ফোঁটা রক্ত, এক জীবন রক্ষা</p>
</div>
</body></html>
"""

@app.route('/', methods=['GET','POST'])
def home():
    conn = sqlite3.connect('roktajoddha.db')
    c = conn.cursor()
    if request.method=='POST':
        c.execute("INSERT INTO donors (name,blood,phone,country,city) VALUES (?,?,?,?,?)",
                  (request.form['name'],request.form['blood'],request.form['phone'],request.form['country'],request.form['city']))
        conn.commit(); conn.close()
        return redirect('/')
    b = request.args.get('blood','')
    city = request.args.get('city','')
    q="SELECT * FROM donors WHERE 1=1"; p=[]
    if b: q+=" AND blood=?"; p.append(b)
    if city: q+=" AND (city LIKE? OR country LIKE?)"; p.extend([f"%{city}%",f"%{city}%"])
    q+=" ORDER BY id DESC"
    c.execute(q,p)
    donors=c.fetchall()
    conn.close()
    return render_template_string(PAGE, donors=donors, city=city)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=10000)
