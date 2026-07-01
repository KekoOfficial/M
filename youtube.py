import yt_dlp
import os
from config import CARPETA_MUSICA, CALIDAD_MP3, MAX_CONEXIONES, RETRIES_DESCARGA, ESPERA_ENTRE_PET
from utils import actualizar_carpeta
from archivos import borrar_duplicados

# Configuración optimizada para YouTube y YouTube Music
OPCIONES_YOUTUBE = {
    "format": "bestaudio/best",
    "outtmpl": f"{CARPETA_MUSICA}/%(playlist_title)s/%(title)s.%(ext)s",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": CALIDAD_MP3
    }],
    "noplaylist": False,
    "quiet": False,
    "no_warnings": False,
    "overwrites": False,
    "concurrent_fragments": MAX_CONEXIONES,
    "buffersize": 2 * 1024 * 1024,
    "retries": RETRIES_DESCARGA,
    "fragment_retries": RETRIES_DESCARGA,
    "sleep_interval": ESPERA_ENTRE_PET,
    "max_sleep_interval": 6,
    "random_sleep": True,
    "extract_flat": "in_playlist",
    "force_generic_extractor": False,
    "extractor_args": {
        "youtube": {
            "player_client": ["android", "web"],
            "player_skip": ["js", "configs"],
            "include_hls": True
        }
    },
    "http_headers": {
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
        "Accept-Language": "es-PY,es;q=0.9,en;q=0.8",
        "Referer": "https://www.youtube.com/",
        "Origin": "https://www.youtube.com"
    }
}


def normalizar_enlace(enlace):
    """Convierte enlaces de YouTube Music a YouTube normal"""
    enlace = enlace.strip()
    if "music.youtube.com" in enlace:
        enlace = enlace.replace("music.youtube.com", "www.youtube.com")
        print("🔄 Redirigiendo desde YouTube Music a YouTube...")
    return enlace


def descargar_youtube(enlace):
    try:
        enlace_corregido = normalizar_enlace(enlace)
        print("🎵 Procesando YouTube / YouTube Music...")

        with yt_dlp.YoutubeDL(OPCIONES_YOUTUBE) as ydl:
            info = ydl.extract_info(enlace_corregido, download=True)

        borrar_duplicados()
        actualizar_carpeta(CARPETA_MUSICA)

        if info.get("_type") == "playlist":
            total = len(info.get("entries", []))
            return True, f"✅ Lista completada | {total} canciones descargadas"
        else:
            return True, f"✅ Canción descargada: {info.get('title', 'Sin título')[:50]}"

    except Exception as e:
        error = str(e).lower()

        if "already exists" in error:
            return False, "⚠️ Ya existe, saltado"
        elif "403" in error or "forbidden" in error:
            return False, "❌ Bloqueo temporal (403) | Esperá unos minutos y probá de nuevo"
        elif "playlist" in error or "tab page" in error:
            return False, "❌ No se pudo leer la lista | Probá actualizar yt-dlp"
        elif "not found" in error:
            return False, "❌ Video no existe o es privado"

        return False, f"❌ Error: {str(e)[:70]}"
