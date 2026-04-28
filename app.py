from flask import Flask, render_template_string, request, redirect, url_for, session
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "clave_secreta_utp_2026" # Necesario para manejar sesiones

# Simulación de base de datos
usuarios_registrados = {} # {username: {datos_personales}}
logs_globales = [
    {"usuario": "SISTEMA", "evento": "Servidor PaaS en línea", "fecha": "2026-04-26 21:00"}
]

HTML_BASE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CloudGuard Pro | Security Management</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
        body { font-family: 'JetBrains Mono', monospace; background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); }
        .glass { background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(12px); border: 1px solid rgba(56, 189, 248, 0.1); }
        .neon-blue { box-shadow: 0 0 20px rgba(14, 165, 233, 0.2); border: 1px solid #0ea5e9; }
        .input-dark { background: #020617; border: 1px solid #1e293b; color: white; transition: all 0.3s; }
        .input-dark:focus { border-color: #38bdf8; box-shadow: 0 0 10px rgba(56, 189, 248, 0.3); outline: none; }
    </style>
</head>
<body class="text-slate-300 min-h-screen flex flex-col">

    <nav class="p-4 glass border-b border-slate-800 flex justify-between items-center px-8">
        <div class="flex items-center space-x-3">
            <div class="bg-sky-500 p-2 rounded-lg"><i class="fas fa-server text-slate-900"></i></div>
            <span class="text-xl font-bold text-white tracking-widest">CLOUDGUARD <span class="text-sky-400">PRO</span></span>
        </div>
        {% if session.get('user') %}
            <div class="flex items-center space-x-4">
                <span class="text-xs text-sky-400 font-bold underline">ID: {{ session['user'] }}</span>
                <a href="/logout" class="text-xs bg-red-500/20 text-red-400 px-3 py-1 rounded hover:bg-red-500 hover:text-white transition">SALIR</a>
            </div>
        {% endif %}
    </nav>

    <main class="flex-grow container mx-auto py-12 px-4">
        {% block content %}{% endblock %}
    </main>

    <footer class="p-6 text-center text-[10px] text-slate-600 border-t border-slate-900">
        <p>PLATFORM AS A SERVICE (PAAS) DEMONSTRATION - UTP CYBERSECURITY LABS 2026</p>
    </footer>
</body>
</html>
'''

# --- VISTA: SELECCIÓN INICIAL ---
INDEX_HTML = '''
{% extends "base" %}
{% block content %}
<div class="max-w-2xl mx-auto text-center mt-10">
    <h1 class="text-4xl font-bold text-white mb-4">Gestión de Accesos PaaS</h1>
    <p class="text-slate-400 mb-10">Sistema centralizado de registro de auditores de ciberseguridad.</p>
    
    <div class="grid md:grid-cols-2 gap-6">
        <a href="/registro" class="glass p-8 rounded-2xl hover:neon-blue transition-all group">
            <i class="fas fa-user-plus text-4xl text-sky-400 mb-4 group-hover:scale-110 transition"></i>
            <h3 class="text-xl font-bold text-white">Nuevo Auditor</h3>
            <p class="text-sm text-slate-500 mt-2">Crear perfil y registrar datos personales.</p>
        </a>
        <a href="/login" class="glass p-8 rounded-2xl hover:neon-blue transition-all group border-emerald-500/20">
            <i class="fas fa-key text-4xl text-emerald-400 mb-4 group-hover:scale-110 transition"></i>
            <h3 class="text-xl font-bold text-white">Auditor Existente</h3>
            <p class="text-sm text-slate-500 mt-2">Acceder a la base de logs de seguridad.</p>
        </a>
    </div>
</div>
{% endblock %}
'''

# --- VISTA: REGISTRO (FORMULARIO GRANDE) ---
REGISTRO_HTML = '''
{% extends "base" %}
{% block content %}
<div class="max-w-xl mx-auto glass p-8 rounded-2xl neon-blue">
    <h2 class="text-2xl font-bold text-white mb-6 border-b border-slate-800 pb-4">Registro de Nuevo Auditor</h2>
    <form action="/crear_perfil" method="POST" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
            <div>
                <label class="text-[10px] text-sky-400 font-bold">NOMBRE COMPLETO</label>
                <input type="text" name="nombre" required class="w-full p-3 rounded-lg input-dark mt-1">
            </div>
            <div>
                <label class="text-[10px] text-sky-400 font-bold">CÉDULA / ID</label>
                <input type="text" name="cedula" required class="w-full p-3 rounded-lg input-dark mt-1">
            </div>
        </div>
        <div class="grid grid-cols-2 gap-4">
            <div>
                <label class="text-[10px] text-sky-400 font-bold">EDAD</label>
                <input type="number" name="edad" required class="w-full p-3 rounded-lg input-dark mt-1">
            </div>
            <div>
                <label class="text-[10px] text-sky-400 font-bold">LICENCIATURA</label>
                <input type="text" name="licenciatura" required placeholder="Ciberseguridad" class="w-full p-3 rounded-lg input-dark mt-1">
            </div>
        </div>
        <div>
            <label class="text-[10px] text-sky-400 font-bold">UNIVERSIDAD</label>
            <input type="text" name="universidad" required value="Universidad Tecnológica de Panamá" class="w-full p-3 rounded-lg input-dark mt-1">
        </div>
        <div class="bg-sky-500/10 p-4 rounded-lg border border-sky-500/30">
            <label class="text-[10px] text-sky-400 font-bold">DEFINA SU USERNAME DE ACCESO</label>
            <input type="text" name="username" required class="w-full p-3 rounded-lg input-dark mt-1 border-sky-500/50">
        </div>
        <button type="submit" class="w-full bg-sky-600 hover:bg-sky-500 text-white font-bold py-4 rounded-xl transition">COMPLETAR REGISTRO</button>
    </form>
</div>
{% endblock %}
'''

# --- VISTA: DASHBOARD DE LOGS (PROTEGIDO) ---
DASHBOARD_HTML = '''
{% extends "base" %}
{% block content %}
<div class="grid lg:grid-cols-4 gap-6">
    <div class="lg:col-span-1 space-y-6">
        <div class="glass p-6 rounded-xl border-l-4 border-sky-500">
            <h4 class="text-sky-400 font-bold text-xs">PERFIL ACTIVO</h4>
            <p class="text-white text-lg font-bold mt-2">{{ datos.nombre }}</p>
            <p class="text-slate-500 text-xs">{{ datos.licenciatura }}</p>
        </div>
        <div class="glass p-6 rounded-xl">
            <h4 class="text-xs font-bold text-slate-500 mb-4">AÑADIR HALLAZGO</h4>
            <form action="/nuevo_log" method="POST" class="space-y-3">
                <textarea name="evento" required class="w-full bg-slate-900 border border-slate-800 rounded p-2 text-sm text-white" placeholder="Describa evento..."></textarea>
                <button class="w-full bg-sky-600 py-2 rounded text-xs font-bold text-white hover:bg-sky-400 transition">POST LOG</button>
            </form>
        </div>
    </div>
    <div class="lg:col-span-3">
        <div class="glass rounded-xl overflow-hidden">
            <div class="p-4 border-b border-slate-800 bg-slate-900/50 flex justify-between">
                <span class="font-bold text-white">REPOSITORIO GLOBAL DE LOGS</span>
                <span class="text-emerald-400 text-xs tracking-widest animate-pulse">● LIVE FEED</span>
            </div>
            <div class="overflow-y-auto max-h-[500px]">
                <table class="w-full text-left">
                    <thead class="text-[10px] text-slate-500 uppercase">
                        <tr class="border-b border-slate-800">
                            <th class="p-4">Fecha</th>
                            <th class="p-4">Autor</th>
                            <th class="p-4">Evento</th>
                        </tr>
                    </thead>
                    <tbody class="text-sm divide-y divide-slate-800/50">
                        {% for item in logs %}
                        <tr class="hover:bg-sky-500/5 transition-colors">
                            <td class="p-4 text-slate-500 text-xs">{{ item.fecha }}</td>
                            <td class="p-4 text-sky-400 font-bold">{{ item.usuario }}</td>
                            <td class="p-4 text-slate-300 italic">"{{ item.evento }}"</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

# --- RUTAS ---
@app.route('/')
def home():
    return render_template_string(HTML_BASE + INDEX_HTML)

@app.route('/registro')
def registro():
    return render_template_string(HTML_BASE + REGISTRO_HTML)

@app.route('/login')
def login_view():
    return render_template_string(HTML_BASE + '''
    {% extends "base" %}
    {% block content %}
    <div class="max-w-sm mx-auto glass p-8 rounded-2xl neon-blue text-center">
        <i class="fas fa-user-shield text-4xl text-emerald-400 mb-4"></i>
        <h2 class="text-xl font-bold text-white mb-6">Acceso Auditor</h2>
        <form action="/validar_login" method="POST" class="space-y-4">
            <input type="text" name="username" placeholder="Su Username" required class="w-full p-3 rounded-lg input-dark">
            <button class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3 rounded-xl transition">ENTRAR AL SISTEMA</button>
        </form>
        <a href="/" class="block mt-6 text-xs text-slate-500 hover:text-sky-400 underline">Volver al inicio</a>
    </div>
    {% endblock %}
    ''')

@app.route('/crear_perfil', methods=['POST'])
def crear_perfil():
    username = request.form.get('username')
    usuarios_registrados[username] = {
        "nombre": request.form.get('nombre'),
        "cedula": request.form.get('cedula'),
        "edad": request.form.get('edad'),
        "licenciatura": request.form.get('licenciatura'),
        "universidad": request.form.get('universidad')
    }
    session['user'] = username
    return redirect(url_for('dashboard'))

@app.route('/validar_login', methods=['POST'])
def validar_login():
    username = request.form.get('username')
    if username in usuarios_registrados:
        session['user'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login_view'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('login_view'))
    user_data = usuarios_registrados[session['user']]
    return render_template_string(HTML_BASE + DASHBOARD_HTML, datos=user_data, logs=logs_globales)

@app.route('/nuevo_log', methods=['POST'])
def nuevo_log():
    if 'user' in session:
        evento = request.form.get('evento')
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logs_globales.insert(0, {"usuario": session['user'], "evento": evento, "fecha": fecha})
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
