import yt_dlp
from config import CARPETA_MUSICA, CARPETA_TIKTOK, MAX_CONEXIONES, CALIDAD_MP3
from utils import actualizar_carpeta
from archivos import borrar_duplicados

# Opciones para videos de TikTok
OPCIONES_TIKTOK = {
    "format": "best",
    "outtmpl": f"{CARPETA_TIKTOK}/%(title)s.%(ext)s",
    "noplaylist": True,
    "quiet": False,
    "no_warnings": False,
    "concurrent_fragments": MAX_CONEXIONES,
    "buffersize": 1024 * 1024,
    "retries": 10,
    "fragment_retries": 10,
    "overwrites": False
}

# Opciones para música de YouTube
OPCIONES_MUSICA = {
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
    "skip_download": False,
    "overwrites": False,
    "concurrent_fragments": MAX_CONEXIONES,
    "buffersize": 1024 * 1024,
    "retries": 10,
    "fragment_retries": 10
}

def descargar(enlace):
    """Función principal para iniciar la descarga"""
    try:
        if "tiktok.com" in enlace:
            tipo = "TIKTOK"
            carpeta = CARPETA_TIKTOK
            opciones = OPCIONES_TIKTOK
        else:
            tipo = "MUSICA"
            carpeta = CARPETA_MUSICA
            opciones = OPCIONES_MUSICA

        print(f"📥 Descargando {tipo}: {enlace[:60]}...")

        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.extract_info(enlace, download=True)

        if tipo == "MUSICA":
            borrar_duplicados()

        actualizar_carpeta(carpeta)
        return True, f"✅ {tipo} completado"

    except Exception as e:
        if "already exists" in str(e):
            return False, "⚠️ Ya existe, saltado"
        return False, f"❌ Error: {str(e)[:80]}"
