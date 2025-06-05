# subdomainfinder
Repositorio destinado a scripts en diversas tecnologías para listar subdominios

🔎 Descripción
subdomain_enum_extended.py es una herramienta avanzada de enumeración pasiva de subdominios escrita en Python. Combina múltiples fuentes OSINT y herramientas externas para descubrir subdominios de un dominio objetivo, identificar cuáles están activos y guardar los resultados en archivos estructurados.

Propósito
Esta herramienta es útil para:

Recolección pasiva de inteligencia (OSINT)

Reconocimiento en pruebas de penetración (fase de recon)

Identificación rápida de subdominios expuestos y servicios activos

⚙️ Funcionalidades
Consulta múltiples fuentes OSINT:

crt.sh

certspotter (SSLMate)

rapiddns.io

Integra herramientas locales si están disponibles:

subfinder (descubrimiento masivo rápido)

amass (modo pasivo, tiempo limitado a 10 min)

httpx (para identificar subdominios vivos)

Guarda:

Subdominios encontrados

Subdominios vivos

Logs detallados (amass, httpx)

📦 Dependencias
🔸 Python
Python 3

Módulos:

bash
Copiar
Editar
pip3 install requests

🔸 Herramientas externas (opcionales pero recomendadas)
Herramienta	Función	Instalación
subfinder	Enumeración rápida de subdominios	Instrucciones
amass	Enumeración pasiva desde múltiples fuentes	sudo apt install amass
httpx	Verificación masiva de servicios activos	go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

Asegúrate de que $HOME/go/bin esté en tu $PATH para usar herramientas Go como httpx.

🧪 Uso
bash
Copiar
Editar
python3 subdomain_enum_extended.py <dominio>

📍 Ejemplo:
bash
Copiar
Editar
python3 subdomain_enum_extended.py google.com

📁 Archivos generados
subdomains_<dominio>.txt
Contiene todos los subdominios encontrados y los que están vivos.

amass_output.txt
Contiene toda la salida generada por amass, incluso si se interrumpe a los 10 minutos.

httpx_live.txt
Contiene los resultados detallados de subdominios vivos detectados por httpx.

🛡️ Legalidad y uso ético
Esta herramienta es solo para uso autorizado y ético.
Úsala exclusivamente en dominios de tu propiedad o con autorización explícita.
La recopilación pasiva de subdominios es legal en muchos contextos, pero tú eres responsable de tu uso.

🙌 Autor / Mantenimiento
Script personalizado con integración OSINT por David Delgado Déniz.
Puedes modificarlo para agregar otras fuentes o automatizar escaneo de puertos, tecnologías, etc.
