from flask import Flask, render_template_string
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
        <body style="font-family:sans-serif; background:#0f172a; color:white; text-align:center; padding-top:100px;">
            <div style="border:2px solid #38bdf8; display:inline-block; padding:40px; border-radius:20px; box-shadow: 0 0 20px #38bdf8;">
                <h1 style="color:#38bdf8; margin-bottom:10px;">PaaS Security Dashboard</h1>
                <p style="font-size:1.2em;">Estado: <span style="color:#4ad361;">● ACTIVE</span></p>
                <hr style="border:0; border-top:1px solid #334155; margin:20px 0;">
                <p>Plataforma: <strong>DigitalOcean App Platform</strong></p>
                <p>Ubicación: <strong>Cloud Managed Runtime</strong></p>
                <p style="color:#94a3b8; font-size:0.8em; margin-top:30px;">Proyecto de Ciberseguridad - Universidad Tecnológica de Panamá</p>
            </div>
        </body>
    ''')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)