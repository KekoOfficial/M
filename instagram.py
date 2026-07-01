import yt_dlp
import os
import time
import random
from config import (
    CARPETA_INSTAGRAM, CALIDAD_MP4, MAX_CONEXIONES,
    ARCHIVO_COOKIES, REINTENTOS, ESPERA_ENTRE_PET, PAIS_GEOBYPASS
)
from utils import actualizar_carpeta, escribir_error, limpiar_nombre

# Lista de agentes para evitar bloqueos
USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36"
]

# Configuración optimizada
OPCIONES_INSTAGRAM = {
    "format": CALIDAD_MP4,
    "merge_output_format": "mp4",
    "outtmpl": f"{CARPETA_INSTAGRAM}/%(id)s_{limpiar_nombre('%(title)s')}.%(ext)s",
    "noplaylist": True,
    "quiet": False,
    "no_warnings": False,
    "overwrites": False,
    "continuedl": True,
    "concurrent_fragments": min(MAX_CONEXIONES, 4),
    "buffersize": 2 * 1024 * 1024,
    "retries": REINTENTOS,
    "fragment_retries": REINTENTOS,
    "sleep_interval": ESPERA_ENTRE_PET,
    "max_sleep_interval": ESPERA_ENTRE_PET * 3,
    "random_sleep": True,
    "geo_bypass": True,
    "geo_bypass_country": PAIS_GEOBYPASS,
    "extractor_args": {
        "instagram": {
            "api_version": "v24",
            "include_ads": False,
            "skip_extra_formats": True
        }
    },
    "http_headers": {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/json,*/*;q=0.8",
        "Accept-Language": "es-PY,es;q=0.9,en;q=0.8",
        "Referer": "https://www.instagram.com/",
        "Origin": "https://www.instagram.com"
    }
}

# Cargar cookies si existen
COOKIES_CARGADAS = False
if os.path.isfile(ARCHIVO_COOKIES) and os.path.getsize(ARCHIVO_COOKIES) > 20:
    OPCIONES_INSTAGRAM["cookiefile"] = ARCHIVO_COOKIES
    COOKIES_CARGADAS = True
    print("🍪 Cookies de Instagram cargadas correctamente")
else:
    print("ℹ️ Sin cookies: solo funcionarán perfiles públicos sin inicio de sesión")


def descargar_instagram(enlace):
    intentos = 0
    max_intentos = 3
    enlace = enlace.strip()

    while intentos < max_intentos:
        try:
            print("📸 Procesando Instagram...")
            with yt_dlp.YoutubeDL(OPCIONES_INSTAGRAM) as ydl:
                info = ydl.extract_info(enlace, download=True)

            actualizar_carpeta(CARPETA_INSTAGRAM)
            return True, f"✅ Instagram descargado: {info.get('title', 'Sin título')[:50]}"

        except Exception as e:
            intentos += 1
            error = str(e).lower()

            if "already exists" in error:
                return False, "⚠️ Ya existe, saltado"
            elif "404" in error or "not found" in error:
                return False, "❌ Video no existe o eliminado"
            elif "empty media" in error or "login required" in error or "private" in error:
                if COOKIES_CARGADAS:
                    escribir_error(f"Instagram: Cookies vencidas | {enlace}")
                    return False, "❌ Cookies vencidas: generá nuevas"
                else:
                    return False, "❌ Requiere inicio de sesión: agregá cookies"

            escribir_error(f"Instagram error: {enlace} | {str(e)[:100]}")
            if intentos < max_intentos:
                time.sleep(3 * intentos)
                continue
            return False, f"❌ Error: {str(e)[:70]}"

    return False, "❌ Se agotaron los intentos"
