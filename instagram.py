import yt_dlp
import os
from config import CARPETA_INSTAGRAM, CALIDAD_MP4, MAX_CONEXIONES, ARCHIVO_COOKIES, REINTENTOS, ESPERA_ENTRE_PET
from utils import actualizar_carpeta

OPCIONES_INSTAGRAM = {
    "format": CALIDAD_MP4,
    "merge_output_format": "mp4",
    "outtmpl": f"{CARPETA_INSTAGRAM}/%(id)s_%(title).70s.%(ext)s",
    "noplaylist": True,
    "quiet": False,
    "no_warnings": False,
    "overwrites": False,
    "concurrent_fragments": MAX_CONEXIONES,
    "buffersize": 2 * 1024 * 1024,
    "retries": REINTENTOS,
    "fragment_retries": REINTENTOS,
    "sleep_interval": ESPERA_ENTRE_PET,
    "max_sleep_interval": 5,
    "random_sleep": True,
    "geo_bypass": True,
    "geo_bypass_country": "PY",
    "extractor_args": {"instagram": {"api_version": "v21"}},
    "http_headers": {
        "User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
        "Accept-Language": "es-PY,es;q=0.9,en;q=0.8",
        "Referer": "https://www.instagram.com/"
    }
}

# Cargar cookies solo si existen
if os.path.exists(ARCHIVO_COOKIES) and os.path.getsize(ARCHIVO_COOKIES) > 10:
    OPCIONES_INSTAGRAM["cookiefile"] = ARCHIVO_COOKIES
    COOKIES_CARGADAS = True
else:
    COOKIES_CARGADAS = False


def descargar_instagram(enlace):
    try:
        print("📸 Procesando Instagram...")
        with yt_dlp.YoutubeDL(OPCIONES_INSTAGRAM) as ydl:
            ydl.extract_info(enlace, download=True)
        actualizar_carpeta(CARPETA_INSTAGRAM)
        return True, "✅ Instagram descargado correctamente"

    except Exception as e:
        error = str(e).lower()
        if "already exists" in error:
            return False, "⚠️ Ya existe, saltado"
        elif "empty media" in error or "login required" in error:
            if COOKIES_CARGADAS:
                return False, "❌ Cookies vencidas → generá nuevas"
            else:
                return False, "❌ Falta archivo cookies_instagram.txt"
        return False, f"❌ Error: {str(e)[:70]}"
