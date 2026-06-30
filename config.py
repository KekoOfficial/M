import os

# Rutas de guardado
CARPETA_MUSICA    = "/data/data/com.termux/files/home/storage/shared/Musica"
CARPETA_TIKTOK    = "/data/data/com.termux/files/home/storage/shared/TikTok"
CARPETA_INSTAGRAM = "/data/data/com.termux/files/home/storage/shared/Instagram"
CARPETA_FACEBOOK  = "/data/data/com.termux/files/home/storage/shared/Facebook"

# Configuración
ARCHIVO_COOKIES = "./cookies_instagram.txt"
MAX_CONEXIONES  = 10
CALIDAD_MP3     = "320"
CALIDAD_MP4     = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"

contador_duplicados = 0

# Crear carpetas automáticamente
for carpeta in [CARPETA_MUSICA, CARPETA_TIKTOK, CARPETA_INSTAGRAM, CARPETA_FACEBOOK]:
    os.makedirs(carpeta, exist_ok=True)
