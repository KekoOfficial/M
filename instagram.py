import yt_dlp
import os
from config import CARPETA_INSTAGRAM, CALIDAD_MP4, MAX_CONEXIONES, ARCHIVO_COOKIES
from utils import actualizar_carpeta, tiene_cookies

OPCIONES_INSTAGRAM = {
    "format": CALIDAD_MP4,
    "merge_output_format": "mp4",
    "outtmpl": f"{CARPETA_INSTAGRAM}/%(title)s.%(ext)s",
    "noplaylist": True,
    "quiet": False,
    "no_warnings": False,
    "overwrites": False,
    "concurrent_fragments": MAX_CONEXIONES,
    "buffersize": 1024 * 1024,
    "retries": 15,
    "geo_bypass": True,
    "geo_bypass_country": "PY",
    "http_headers": {
        "User-Agent": "Mozilla/5.0 (Linux; Android 14) Chrome/128.0.0.0 Mobile Safari/537.36"
    }
}

# Agregar cookies si existen
if tiene_cookies():
    OPCIONES_INSTAGRAM["cookiefile"] = ARCHIVO_COOKIES

def descargar_instagram(enlace):
    try:
        print("📸 Procesando Instagram...")
        with yt_dlp.YoutubeDL(OPCIONES_INSTAGRAM) as ydl:
            ydl.extract_info(enlace, download=True)

        actualizar_carpeta(CARPETA_INSTAGRAM)
        return True, "✅ Instagram MP4 listo"

    except Exception as e:
        error = str(e).lower()
        if "already exists" in error:
            return False, "⚠️ Instagram: Ya existe"
        elif "empty media" in error or "login required" in error:
            return False, "❌ Instagram: Necesita cookies válidas"
        return False, f"❌ Instagram: {str(e)[:70]}"
