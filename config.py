import os

# Rutas Termux
CARPETA_MUSICA    = "/data/data/com.termux/files/home/storage/shared/Musica"
CARPETA_FACEBOOK  = "/data/data/com.termux/files/home/storage/shared/Facebook"
CARPETA_WHATSAPP  = "/data/data/com.termux/files/home/storage/shared/WhatsApp"
CARPETA_INSTAGRAM = "/data/data/com.termux/files/home/storage/shared/Instagram"
CARPETA_TIKTOK    = "/data/data/com.termux/files/home/storage/shared/TikTok"
CARPETA_X         = "/data/data/com.termux/files/home/storage/shared/X_Twitter"
CARPETA_TELEGRAM  = "/data/data/com.termux/files/home/storage/shared/Telegram"
CARPETA_LINKEDIN  = "/data/data/com.termux/files/home/storage/shared/LinkedIn"
CARPETA_DISCORD   = "/data/data/com.termux/files/home/storage/shared/Discord"
CARPETA_SNAPCHAT  = "/data/data/com.termux/files/home/storage/shared/Snapchat"
CARPETA_PINTEREST = "/data/data/com.termux/files/home/storage/shared/Pinterest"
CARPETA_THREADS   = "/data/data/com.termux/files/home/storage/shared/Threads"
CARPETA_REDDIT    = "/data/data/com.termux/files/home/storage/shared/Reddit"
CARPETA_MESSENGER = "/data/data/com.termux/files/home/storage/shared/Messenger"
CARPETA_BIGOLIVE  = "/data/data/com.termux/files/home/storage/shared/BigoLive"
CARPETA_OTROS     = "/data/data/com.termux/files/home/storage/shared/Otros"

ARCHIVO_ESTADO = "estado_descarga.txt"
MAX_CONEXIONES = 10
CALIDAD_MP3    = "320"
CALIDAD_MP4    = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"

contador_duplicados = 0

# Crear todas las carpetas
for carpeta in [
    CARPETA_MUSICA, CARPETA_FACEBOOK, CARPETA_WHATSAPP, CARPETA_INSTAGRAM,
    CARPETA_TIKTOK, CARPETA_X, CARPETA_TELEGRAM, CARPETA_LINKEDIN,
    CARPETA_DISCORD, CARPETA_SNAPCHAT, CARPETA_PINTEREST, CARPETA_THREADS,
    CARPETA_REDDIT, CARPETA_MESSENGER, CARPETA_BIGOLIVE, CARPETA_OTROS
]:
    os.makedirs(carpeta, exist_ok=True)
