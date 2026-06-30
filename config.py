import os

# ─────────────────────────────────────────────────────
# 📁 RUTAS DE ALMACENAMIENTO (Termux / Android)
# ─────────────────────────────────────────────────────
# Se guardan en la carpeta compartida accesible desde la galería
CARPETA_MUSICA    = "/data/data/com.termux/files/home/storage/shared/Musica"
CARPETA_TIKTOK    = "/data/data/com.termux/files/home/storage/shared/TikTok"
CARPETA_INSTAGRAM = "/data/data/com.termux/files/home/storage/shared/Instagram"
CARPETA_FACEBOOK  = "/data/data/com.termux/files/home/storage/shared/Facebook"

# ─────────────────────────────────────────────────────
# 🔐 ARCHIVOS DE SOPORTE
# ─────────────────────────────────────────────────────
ARCHIVO_ESTADO    = "/data/data/com.termux/files/home/descargador-multired/estado_descarga.txt"
ARCHIVO_ERRORES   = "/data/data/com.termux/files/home/descargador-multired/errores.log"
ARCHIVO_COOKIES   = "/data/data/com.termux/files/home/descargador-multired/cookies_instagram.txt"

# ─────────────────────────────────────────────────────
# ⚙️ CONFIGURACIÓN GENERAL
# ─────────────────────────────────────────────────────
MAX_CONEXIONES    = 12               # Conexiones simultáneas
CALIDAD_MP3       = "320"           # Calidad máxima MP3 para YouTube
CALIDAD_MP4       = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
RETRIES_DESCARGA  = 25               # Intentos si falla la descarga
TIEMPO_ESPERA     = 2                # Segundos de espera entre peticiones

# ─────────────────────────────────────────────────────
# 📊 CONTADORES GLOBALES
# ─────────────────────────────────────────────────────
contador_duplicados = 0
contador_descargas = 0
contador_errores    = 0

# ─────────────────────────────────────────────────────
# 🚀 CREACIÓN AUTOMÁTICA DE CARPETAS
# ─────────────────────────────────────────────────────
for carpeta in [
    CARPETA_MUSICA,
    CARPETA_TIKTOK,
    CARPETA_INSTAGRAM,
    CARPETA_FACEBOOK
]:
    try:
        os.makedirs(carpeta, exist_ok=True)
    except Exception as e:
        print(f"⚠️ No se pudo crear carpeta {carpeta}: {e}")
