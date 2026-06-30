import yt_dlp
import os
from config import CARPETA_INSTAGRAM, CALIDAD_MP4, MAX_CONEXIONES, ARCHIVO_COOKIES
from utils import actualizar_carpeta

# Configuración optimizada para Instagram
OPCIONES_INSTAGRAM = {
    "format": CALIDAD_MP4,
    "merge_output_format": "mp4",
    "outtmpl": f"{CARPETA_INSTAGRAM}/%(id)s_%(title).80s.%(ext)s",
    "noplaylist": True,
    "quiet": False,
    "no_warnings": False,
    "overwrites": False,
    "concurrent_fragments": MAX_CONEXIONES,
    "buffersize": 2 * 1024 * 1024,
    "retries": 25,
    "fragment_retries": 25,
    "sleep_interval": 2,
    "max_sleep_interval": 6,
    "random_sleep_interval": True,
    "geo_bypass": True,
    "geo_bypass_country": "PY",
    "extractor_args": {
        "instagram": {
            "include_ads": False,
            "api_version": "v19",
            "skip_extra_formats": True
        }
    },
    "http_headers": {
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
        "Accept": "text/html,application/json,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "es-PY,es;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.instagram.com/",
        "Origin": "https://www.instagram.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty"
    }
}

# Cargar cookies si existen
cargado_cookies = False
if os.path.isfile(ARCHIVO_COOKIES) and os.path.getsize(ARCHIVO_COOKIES) > 10:
    OPCIONES_INSTAGRAM["cookiefile"] = ARCHIVO_COOKIES
    cargado_cookies = True


def descargar_instagram(enlace):
    try:
        print("📸 Procesando enlace de Instagram...")

        with yt_dlp.YoutubeDL(OPCIONES_INSTAGRAM) as ydl:
            info = ydl.extract_info(enlace, download=True)

        actualizar_carpeta(CARPETA_INSTAGRAM)
        return True, f"✅ Instagram listo | Archivo guardado"

    except Exception as e:
        error = str(e).lower()

        if "already exists" in error:
            return False, "⚠️ Ya existe, saltado"

        elif "empty media" in error or "login required" in error or "private" in error:
            if cargado_cookies:
                return False, "❌ Cookies vencidas | Generá nuevas"
            else:
                return False, "❌ Falta archivo cookies_instagram.txt"

        elif "not found" in error or "does not exist" in error:
            return False, "❌ Video no existe o es privado"

        return False, f"❌ Error: {str(e)[:70]}"
