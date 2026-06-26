import yt_dlp
from config import *
from utils import actualizar_carpeta
from archivos import borrar_duplicados

# Opciones exclusivas YouTube → MP3
OPCIONES_MP3 = {
    "format": "bestaudio/best",
    "outtmpl": f"{CARPETA_MUSICA}/%(playlist_title)s/%(title)s.%(ext)s",
    "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": CALIDAD_MP3}],
    "noplaylist": False, "quiet": False, "no_warnings": False, "overwrites": False,
    "concurrent_fragments": MAX_CONEXIONES, "buffersize": 1024*1024, "retries": 10,
    "http_headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36"}
}

# Opciones para TODAS las demás → MP4
OPCIONES_MP4 = {
    "format": CALIDAD_MP4,
    "merge_output_format": "mp4",
    "outtmpl": "%(carpeta)s/%(title)s.%(ext)s",
    "noplaylist": True, "quiet": False, "no_warnings": False, "overwrites": False,
    "concurrent_fragments": MAX_CONEXIONES, "buffersize": 1024*1024, "retries": 10,
    "http_headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36"}
}

def detectar_red(enlace):
    enlace = enlace.lower().strip()
    if "youtube.com" in enlace or "youtu.be" in enlace:
        return "YOUTUBE", CARPETA_MUSICA, OPCIONES_MP3
    elif "facebook.com" in enlace or "fb.watch" in enlace:
        return "FACEBOOK", CARPETA_FACEBOOK, OPCIONES_MP4
    elif "wa.me" in enlace or "whatsapp.com" in enlace:
        return "WHATSAPP", CARPETA_WHATSAPP, OPCIONES_MP4
    elif "instagram.com" in enlace or "instagr.am" in enlace:
        return "INSTAGRAM", CARPETA_INSTAGRAM, OPCIONES_MP4
    elif "tiktok.com" in enlace:
        return "TIKTOK", CARPETA_TIKTOK, OPCIONES_MP4
    elif "x.com" in enlace or "twitter.com" in enlace:
        return "X_TWITTER", CARPETA_X, OPCIONES_MP4
    elif "t.me" in enlace or "telegram.org" in enlace:
        return "TELEGRAM", CARPETA_TELEGRAM, OPCIONES_MP4
    elif "linkedin.com" in enlace:
        return "LINKEDIN", CARPETA_LINKEDIN, OPCIONES_MP4
    elif "discord.com" in enlace or "discordapp.com" in enlace:
        return "DISCORD", CARPETA_DISCORD, OPCIONES_MP4
    elif "snapchat.com" in enlace:
        return "SNAPCHAT", CARPETA_SNAPCHAT, OPCIONES_MP4
    elif "pinterest.com" in enlace:
        return "PINTEREST", CARPETA_PINTEREST, OPCIONES_MP4
    elif "threads.net" in enlace:
        return "THREADS", CARPETA_THREADS, OPCIONES_MP4
    elif "reddit.com" in enlace or "redd.it" in enlace:
        return "REDDIT", CARPETA_REDDIT, OPCIONES_MP4
    elif "messenger.com" in enlace or "m.me" in enlace:
        return "MESSENGER", CARPETA_MESSENGER, OPCIONES_MP4
    elif "bigolive.tv" in enlace or "bigolive.com" in enlace:
        return "BIGO_LIVE", CARPETA_BIGOLIVE, OPCIONES_MP4
    else:
        return "OTROS", CARPETA_OTROS, OPCIONES_MP4

def descargar(enlace):
    try:
        tipo, carpeta, opciones = detectar_red(enlace)
        if opciones is OPCIONES_MP4:
            opciones = opciones.copy()
            opciones["outtmpl"] = opciones["outtmpl"].replace("%(carpeta)s", carpeta)

        print(f"📥 {tipo}: {enlace[:65]}...")
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.extract_info(enlace, download=True)

        if tipo == "YOUTUBE":
            borrar_duplicados()
        actualizar_carpeta(carpeta)
        return True, f"✅ {tipo} completado"

    except Exception as e:
        msg = str(e).lower()
        if "already exists" in msg:
            return False, "⚠️ Ya existe, saltado"
        return False, f"❌ Error: {str(e)[:80]}"
