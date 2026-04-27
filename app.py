from flask import Flask, render_template_string, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

# Base de datos en memoria para demostrar persistencia en la sesión
logs_auditoria = [
    {"usuario": "SISTEMA", "hallazgo": "Despliegue PaaS inicializado correctamente.", "tipo": "INFO", "fecha": "2026-04-26 21:00"},
    {"usuario": "FIREWALL", "hallazgo": "Certificado SSL (HTTPS) auto-gestionado activo.", "tipo": "SUCCESS", "fecha": "2026-04-26 21:05"}
]

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CloudGuard PaaS | Security Suite</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap');
        body { font-family: 'Space Mono', monospace; background-color: #020617; }
        .glass { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(56, 189, 248, 0.2); }
        .glow-text { text-shadow: 0 0 10px rgba(56, 189, 248, 0.5); }
        .neon-border { border: 1px solid #0ea5e9; box-shadow: 0 0 15px rgba(14, 165, 233, 0.3); }
    </style>
</head>
<body class="text-slate-200 min-h-screen">

    <nav class="border-b border-slate-800 p-4 glass sticky top-0 z-50">
        <div class="container mx-auto flex justify-between items-center">
            <div class="flex items-center space-x-2">
                <i class="fas fa-shield-halved text-sky-400 text-2xl"></i>
                <span class="text-xl font-bold tracking-tighter glow-text">CLOUDGUARD <span class="text-sky-400">PaaS</span></span>
            </div>
            <div class="hidden md:flex space-x-6 text-sm font-bold">
                <span class="text-green-400"><i class="fas fa-circle text-[8px] mr-1"></i> RUNNING ON DIGITALOCEAN</span>
                <span class="text-slate-400">STATUS: SECURE</span>
            </div>
        </div>
    </nav>

    <main class="container mx-auto py-10 px-4">
        <div class="grid lg:grid-cols-3 gap-8">
            
            <div class="lg:col-span-1">
                <div class="glass p-6 rounded-2xl neon-border">
                    <h2 class="text-xl font-bold mb-6 flex items-center">
                        <i class="fas fa-terminal mr-2 text-sky-400"></i> ENTRADA DE DATOS
                    </h2>
                    <form action="/add_log" method="POST" class="space-y-4">
                        <div>
                            <label class="block text-xs text-sky-400 mb-1 font-bold">ID DEL AUDITOR</label>
                            <input type="text" name="usuario" required placeholder="p.ej. UTP-SEC-01" 
                                class="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white focus:outline-none focus:border-sky-500 transition-all">
                        </div>
                        <div>
                            <label class="block text-xs text-sky-400 mb-1 font-bold">HALLAZGO / REPORTE</label>
                            <textarea name="hallazgo" required placeholder="Describa la vulnerabilidad..." rows="4"
                                class="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white focus:outline-none focus:border-sky-500 transition-all"></textarea>
                        </div>
                        <div>
                            <label class="block text-xs text-sky-400 mb-1 font-bold">NIVEL DE RIESGO</label>
                            <select name="tipo" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white">
                                <option value="INFO">INFORMACIÓN (AZUL)</option>
                                <option value="SUCCESS">ÉXITO (VERDE)</option>
                                <option value="WARNING">CRÍTICO (ROJO)</option>
                            </select>
                        </div>
                        <button type="submit" class="w-full bg-sky-600 hover:bg-sky-500 text-white font-bold py-3 rounded-lg transition-all transform hover:scale-[1.02]">
                            ENVIAR A LA NUBE <i class="fas fa-paper-plane ml-1"></i>
                        </button>
                    </form>
                </div>
            </div>

            <div class="lg:col-span-2">
                <div class="glass p-6 rounded-2xl overflow-hidden border border-slate-800">
                    <h2 class="text-xl font-bold mb-6 flex items-center justify-between">
                        <span><i class="fas fa-database mr-2 text-sky-400"></i> LOGS DE PERSISTENCIA</span>
                        <span class="text-xs bg-slate-800 px-3 py-1 rounded-full text-slate-400 font-normal">Base de Datos: In-Memory DB</span>
                    </h2>
                    
                    <div class="overflow-x-auto">
                        <table class="w-full text-left">
                            <thead>
                                <tr class="text-sky-400 text-xs border-b border-slate-800">
                                    <th class="pb-4">TIMESTAMP</th>
                                    <th class="pb-4">USER_ID</th>
                                    <th class="pb-4">REPORT_LOG</th>
                                    <th class="pb-4">STATUS</th>
                                </tr>
                            </thead>
                            <tbody class="text-sm divide-y divide-slate-800">
                                {% for log in logs %}
                                <tr class="hover:bg-slate-800/50 transition-colors">
                                    <td class="py-4 text-slate-500 text-xs">{{ log.fecha }}</td>
                                    <td class="py-4 font-bold text-sky-200">{{ log.usuario }}</td>
                                    <td class="py-4 text-slate-300">{{ log.hallazgo }}</td>
                                    <td class="py-4">
                                        {% if log.tipo == 'INFO' %}
                                            <span class="bg-blue-500/20 text-blue-400 px-2 py-1 rounded text-[10px] font-bold border border-blue-500/30">INFO</span>
                                        {% elif log.tipo == 'SUCCESS' %}
                                            <span class="bg-green-500/20 text-green-400 px-2 py-1 rounded text-[10px] font-bold border border-green-500/30">SUCCESS</span>
                                        {% else %}
                                            <span class="bg-red-500/20 text-red-400 px-2 py-1 rounded text-[10px] font-bold border border-red-500/30">CRITICAL</span>
                                        {% endif %}
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

        </div>
    </main>

    <footer class="container mx-auto p-10 text-center text-slate-600 text-xs mt-10 border-t border-slate-900">
        <p>AUDITORÍA DE INFRAESTRUCTURA PaaS - CURSO DE CIBERSEGURIDAD 2026</p>
        <p class="mt-2">DESPLEGADO MEDIANTE CONTINUOUS DEPLOYMENT (CI/CD) EN DIGITALOCEAN APP PLATFORM</p>
    </footer>

</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, logs=logs_auditoria)

@app.route('/add_log', methods=['POST'])
def add_log():
    usuario = request.form.get('usuario')
    hallazgo = request.form.get('hallazgo')
    tipo = request.form.get('tipo')
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    logs_auditoria.insert(0, {"usuario": usuario, "hallazgo": hallazgo, "tipo": tipo, "fecha": fecha})
    return redirect(url_for('index'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
