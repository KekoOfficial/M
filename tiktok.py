import yt_dlp
import time
import random
from config import (
    CARPETA_TIKTOK, CALIDAD_MP4, MAX_CONEXIONES,
    REINTENTOS, ESPERA_ENTRE_PET, PAIS_GEOBYPASS
)
from utils import actualizar_carpeta, escribir_error, limpiar_nombre

USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36"
]

OPCIONES_TIKTOK = {
    "format": CALIDAD_MP4,
    "merge_output_format": "mp4",
    "outtmpl": f"{CARPETA_TIKTOK}/%(id)s_{limpiar_nombre('%(title)s')}.%(ext)s",
    "noplaylist": True,
    "quiet": False,
    "no_warnings": False,
    "overwrites": False,
    "concurrent_fragments": min(MAX_CONEXIONES, 4),
    "retries": REINTENTOS,
    "sleep_interval": ESPERA_ENTRE_PET,
    "geo_bypass": True,
    "geo_bypass_country": PAIS_GEOBYPASS,
    "http_headers": {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": "https://www.tiktok.com/"
    }
}

def descargar_tiktok(enlace):
    try:
        print("🎬 Procesando TikTok...")
        with yt_dlp.YoutubeDL(OPCIONES_TIKTOK) as ydl:
            info = ydl.extract_info(enlace, download=True)
        actualizar_carpeta(CARPETA_TIKTOK)
        return True, "✅ TikTok descargado correctamente"
    except Exception as e:
        escribir_error(f"TikTok error: {enlace} | {str(e)[:100]}")
        return False, f"❌ Error: {str(e)[:70]}"
