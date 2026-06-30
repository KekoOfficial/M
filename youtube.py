import yt_dlp
from config import CARPETA_MUSICA, CALIDAD_MP3, MAX_CONEXIONES
from utils import actualizar_carpeta
from archivos import borrar_duplicados

OPCIONES_YOUTUBE = {
    "format": "bestaudio/best",
    "outtmpl": f"{CARPETA_MUSICA}/%(title)s.%(ext)s",
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
    "buffersize": 1024 * 1024,
    "retries": 15,
    "http_headers": {
        "User-Agent": "Mozilla/5.0 (Linux; Android 14) Chrome/128.0.0.0 Mobile Safari/537.36"
    }
}

def descargar_youtube(enlace):
    try:
        print("🎵 Procesando YouTube...")
        with yt_dlp.YoutubeDL(OPCIONES_YOUTUBE) as ydl:
            ydl.extract_info(enlace, download=True)

        borrar_duplicados()
        actualizar_carpeta(CARPETA_MUSICA)
        return True, "✅ YouTube MP3 listo"

    except Exception as e:
        if "already exists" in str(e).lower():
            return False, "⚠️ YouTube: Ya existe"
        return False, f"❌ YouTube: {str(e)[:70]}"
