import yt_dlp
from config import CARPETA_FACEBOOK, CALIDAD_MP4, MAX_CONEXIONES
from utils import actualizar_carpeta

OPCIONES_FACEBOOK = {
    "format": CALIDAD_MP4,
    "merge_output_format": "mp4",
    "outtmpl": f"{CARPETA_FACEBOOK}/%(title)s.%(ext)s",
    "noplaylist": True,
    "quiet": False,
    "no_warnings": False,
    "overwrites": False,
    "concurrent_fragments": MAX_CONEXIONES,
    "buffersize": 1024 * 1024,
    "retries": 15,
    "http_headers": {
        "User-Agent": "Mozilla/5.0 (Linux; Android 14) Chrome/128.0.0.0 Mobile Safari/537.36"
    }
}

def descargar_facebook(enlace):
    try:
        print("👍 Procesando Facebook...")
        with yt_dlp.YoutubeDL(OPCIONES_FACEBOOK) as ydl:
            ydl.extract_info(enlace, download=True)

        actualizar_carpeta(CARPETA_FACEBOOK)
        return True, "✅ Facebook MP4 listo"

    except Exception as e:
        if "already exists" in str(e).lower():
            return False, "⚠️ Facebook: Ya existe"
        return False, f"❌ Facebook: {str(e)[:70]}"
