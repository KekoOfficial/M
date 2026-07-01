import os
from datetime import datetime

# ─────────────────────────────────────────────────────
# 📁 RUTAS DE ALMACENAMIENTO (Termux / Android)
# Todas accesibles desde la galería del celular
# ─────────────────────────────────────────────────────
CARPETA_RAIZ         = "/data/data/com.termux/files/home/storage/shared/DescargadorMultiRed"
CARPETA_MUSICA       = os.path.join(CARPETA_RAIZ, "Musica")
CARPETA_TIKTOK       = os.path.join(CARPETA_RAIZ, "TikTok")
CARPETA_INSTAGRAM    = os.path.join(CARPETA_RAIZ, "Instagram")
CARPETA_FACEBOOK     = os.path.join(CARPETA_RAIZ, "Facebook")
CARPETA_TEMPORAL     = os.path.join(CARPETA_RAIZ, "Temporal")

# ─────────────────────────────────────────────────────
# 📄 ARCHIVOS DE SOPORTE Y REGISTROS
# ─────────────────────────────────────────────────────
ARCHIVO_COOKIES      = os.path.join(os.path.dirname(__file__), "cookies_instagram.txt")
ARCHIVO_ERRORES      = os.path.join(CARPETA_RAIZ, "errores.log")
ARCHIVO_ESTADO       = os.path.join(CARPETA_RAIZ, "estado_descargas.txt")
ARCHIVO_ESTADISTICAS = os.path.join(CARPETA_RAIZ, "estadisticas.txt")

# ─────────────────────────────────────────────────────
# ⚙️ CONFIGURACIÓN GENERAL AVANZADA
# ✅ NOMBRES COINCIDENTES CON TODOS LOS MÓDULOS
# ─────────────────────────────────────────────────────
# Rendimiento y límites
MAX_CONEXIONES       = 8                  # Equilibrio velocidad / evitar bloqueos
MAX_INTENTOS         = 3                  # Reintentos generales por error
RETRIES_DESCARGA     = 30                 # Reintentos por fragmento de archivo
REINTENTOS           = RETRIES_DESCARGA   # Alias para compatibilidad con todo el código
ESPERA_ENTRE_PET     = 3                  # Segundos entre descargas
ESPERA_403           = 15                 # Tiempo de espera en caso de bloqueo 403
MAX_ESPERA           = 20                 # Tiempo máximo de espera permitido

# Calidad de salida
CALIDAD_MP3          = "320"              # Máxima calidad de audio
CALIDAD_MP4          = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
FORMATO_VIDEO        = "mp4"
FORMATO_AUDIO        = "mp3"

# Región e idioma
PAIS_GEOBYPASS       = "PY"               # Paraguay
IDIOMA_PREFERIDO     = "es-PY,es;q=0.9,en;q=0.8"

# Funcionalidades extra
GUARDAR_TEMPORAL     = False              # Eliminar archivos intermedios
INCORPORAR_METADATOS = True               # Agregar título, artista, etc.
INCORPORAR_MINIATURA = True               # Agregar portada a archivos MP3
SALTAR_ERRORES_LISTAS = True              # No detenerse si falla un elemento de una lista

# ─────────────────────────────────────────────────────
# 📊 VARIABLES GLOBALES DE CONTROL Y ESTADÍSTICAS
# ─────────────────────────────────────────────────────
contador_total_descargas = 0
contador_exitosas        = 0
contador_errores         = 0
contador_duplicados      = 0
hora_inicio              = datetime.now()

# ─────────────────────────────────────────────────────
# 🚀 CREACIÓN AUTOMÁTICA DE CARPETAS CON PERMISOS
# ─────────────────────────────────────────────────────
CARPETAS = [
    CARPETA_RAIZ,
    CARPETA_MUSICA,
    CARPETA_TIKTOK,
    CARPETA_INSTAGRAM,
    CARPETA_FACEBOOK,
    CARPETA_TEMPORAL
]

for carpeta in CARPETAS:
    try:
        os.makedirs(carpeta, exist_ok=True)
        os.chmod(carpeta, 0o755)  # Permisos de lectura/escritura en Termux
    except Exception as e:
        print(f"⚠️ Aviso: No se pudo configurar {carpeta}: {str(e)[:60]}")

# ─────────────────────────────────────────────────────
# ✅ VERIFICACIÓN FINAL AL INICIAR
# ─────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("✅ CONFIGURACIÓN CARGADA CORRECTAMENTE")
    print(f"📂 Carpeta principal: {CARPETA_RAIZ}")
    print(f"🕒 Fecha y hora: {hora_inicio.strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 50)
