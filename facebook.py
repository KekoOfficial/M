import yt_dlp
import time
import random
from config import (
    CARPETA_FACEBOOK, CALIDAD_MP4, MAX_CONEXIONES,
    REINTENTOS, ESPERA_ENTRE_PET, PAIS_GEOBYPASS
)
from utils import actualizar_carpeta, escribir_error, limpiar_nombre

USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36"
]

OPCIONES_FACEBOOK = {
    "format": CALIDAD_MP4,
    "merge_output_format": "mp4",
    "outtmpl": f"{CARPETA_FACEBOOK}/%(id)s_{limpiar_nombre('%(title)s')}.%(ext)s",
    "noplaylist": True,
    "quiet": False,
    "no_warnings": False,
    "overwrites": False,
    "retries": REINTENTOS,
    "sleep_interval": ESPERA_ENTRE_PET,
    "geo_bypass": True,
    "geo_bypass_country": PAIS_GEOBYPASS,
    "http_headers": {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": "https://www.facebook.com/"
    }
}

def descargar_facebook(enlace):
    try:
        print("👍 Procesando Facebook...")
        with yt_dlp.YoutubeDL(OPCIONES_FACEBOOK) as ydl:
            info = ydl.extract_info(enlace, download=True)
        actualizar_carpeta(CARPETA_FACEBOOK)
        return True, "✅ Facebook descargado correctamente"
    except Exception as e:
        escribir_error(f"Facebook error: {enlace} | {str(e)[:100]}")
        return False, f"❌ Error: {str(e)[:70]}"
