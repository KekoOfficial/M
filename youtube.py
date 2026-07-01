import yt_dlp
import os
import time
import random
from config import (
    CARPETA_MUSICA, CALIDAD_MP3, MAX_CONEXIONES,
    REINTENTOS, ESPERA_ENTRE_PET, PAIS_GEOBYPASS,
    INCORPORAR_METADATOS, INCORPORAR_MINIATURA,
    SALTAR_ERRORES_LISTAS, ARCHIVO_ERRORES
)
from utils import actualizar_carpeta, escribir_error, limpiar_nombre
from archivos import borrar_duplicados, registrar_descarga

# ─────────────────────────────────────────────────────────────
# 🎯 CONFIGURACIÓN ANTI-BLOQUEO Y COMPATIBILIDAD
# ─────────────────────────────────────────────────────────────
USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
]

OPCIONES_YOUTUBE = {
    # Formato y calidad
    "format": "bestaudio[ext=m4a]/bestaudio/best",
    "format_sort": ["abr", "asr", "size", "br"],
    "outtmpl": f"{CARPETA_MUSICA}/%(playlist_title|Sin Lista)s/%(artist|Desconocido)s - %(title)s.%(ext)s",
    "outtmpl_na_placeholder": "Desconocido",

    # Conversión a MP3
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": CALIDAD_MP3,
        "nopostoverwrites": False
    }],

    # Miniatura y metadatos
    "writethumbnail": INCORPORAR_MINIATURA,
    "embedthumbnail": INCORPORAR_MINIATURA,
    "addmetadata": INCORPORAR_METADATOS,
    "postprocessor_args": {
        "FFmpegMetadata": ["-id3v2_version", "3"],
        "EmbedThumbnail": ["-metadata", "comment=Descargado con Dola Downloader"]
    },

    # Comportamiento
    "noplaylist": False,
    "extract_flat": False,
    "skip_unavailable_fragments": True,
    "ignoreerrors": SALTAR_ERRORES_LISTAS,
    "overwrites": False,
    "continuedl": True,
    "force_generic_extractor": False,  # ✅ Evita que use extractor genérico
    "check_formats": True,

    # Rendimiento y anti-bloqueo
    "concurrent_fragments": min(MAX_CONEXIONES, 6),
    "buffersize": 4 * 1024 * 1024,
    "retries": REINTENTOS,
    "fragment_retries": REINTENTOS,
    "retry_sleep_functions": {"http": lambda n: ESPERA_ENTRE_PET * (1.5 ** n)},
    "sleep_interval": ESPERA_ENTRE_PET,
    "max_sleep_interval": ESPERA_ENTRE_PET * 3,
    "random_sleep": True,
    "sleep_interval_subtitles": 1,

    # Extracción avanzada
    "extractor_args": {
        "youtube": {
            "player_client": ["android", "web_music", "web"],
            "player_skip": [],
            "include_hls": True,
            "include_dash": True,
            "api_key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
        }
    },

    # Cabeceras seguras
    "http_headers": {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/json,*/*;q=0.8",
        "Accept-Language": "es-PY,es;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.youtube.com/",
        "Origin": "https://www.youtube.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document"
    }
}

# ─────────────────────────────────────────────────────────────
# 🛠️ FUNCIONES AUXILIARES CORREGIDAS
# ─────────────────────────────────────────────────────────────
def normalizar_enlace(enlace: str) -> str:
    """✅ Convierte enlaces y NO rompe listas ni parámetros importantes"""
    enlace = enlace.strip()

    # Convertir YouTube Music a YouTube normal
    if "music.youtube.com" in enlace:
        enlace = enlace.replace("music.youtube.com", "www.youtube.com")
        print("🔄 Convertido: YouTube Music → YouTube")

    # Solo quitar parámetros que no afectan el funcionamiento
    partes = enlace.split("&")
    partes_limpias = []
    for p in partes:
        if not p.startswith(("pp=", "feature=", "si=")) or "list=" in p:
            partes_limpias.append(p)

    enlace_limpio = "&".join(partes_limpias)
    return enlace_limpio

def es_lista(enlace: str) -> bool:
    """✅ Detecta correctamente si es una lista de reproducción"""
    return any(x in enlace for x in ["list=", "/playlist", "playlist?"])

def actualizar_agentes():
    """Cambia User-Agent para evitar bloqueos"""
    OPCIONES_YOUTUBE["http_headers"]["User-Agent"] = random.choice(USER_AGENTS)

# ─────────────────────────────────────────────────────────────
# 🎵 FUNCIÓN PRINCIPAL DE DESCARGA
# ─────────────────────────────────────────────────────────────
def descargar_youtube(enlace: str) -> tuple[bool, str]:
    intentos = 0
    max_intentos = 3
    enlace_ok = normalizar_enlace(enlace)
    es_una_lista = es_lista(enlace_ok)

    # Verificación básica del enlace
    if not enlace_ok.startswith(("https://", "http://")):
        return False, "❌ Enlace inválido"

    while intentos < max_intentos:
        try:
            tipo = "LISTA DE REPRODUCCIÓN" if es_una_lista else "VIDEO / CANCIÓN"
            print(f"🎵 Procesando YouTube {tipo}: {enlace_ok[:75]}...")

            with yt_dlp.YoutubeDL(OPCIONES_YOUTUBE) as ydl:
                info = ydl.extract_info(enlace_ok, download=True)

            # Procesamiento final
            borrar_duplicados()
            actualizar_carpeta(CARPETA_MUSICA)
            registrar_descarga("youtube", info)

            # Mensaje de resultado
            if info and info.get("_type") == "playlist":
                entradas = info.get("entries", [])
                exitosas = sum(1 for e in entradas if e and e.get("filepath"))
                total = len(entradas)
                mensaje = f"✅ Lista completada: {exitosas}/{total} canciones descargadas"
            else:
                titulo = info.get("title", "Sin título") if info else "Desconocido"
                mensaje = f"✅ Descargado: {titulo[:60]}"

            return True, mensaje

        except Exception as e:
            intentos += 1
            error = str(e).lower()
            actualizar_agentes()

            if "already exists" in error:
                return False, "⚠️ Ya existe, saltado"

            elif "403" in error or "forbidden" in error:
                escribir_error(f"YouTube 403: {enlace} | Intento {intentos}")
                if intentos < max_intentos:
                    espera = ESPERA_ENTRE_PET * (4 ** intentos)
                    print(f"⏳ Bloqueo temporal, esperando {int(espera)}s...")
                    time.sleep(espera)
                    continue
                return False, "❌ Bloqueo 403: Esperá 10min y actualizá yt-dlp"

            elif "404" in error or "not found" in error:
                escribir_error(f"YouTube 404: {enlace}")
                return False, "❌ Enlace no válido o contenido eliminado"

            elif "private" in error or "unavailable" in error:
                escribir_error(f"YouTube privado/no disponible: {enlace}")
                return False, "❌ Video privado o no disponible"

            elif "playlist" in error or "tab page" in error:
                escribir_error(f"YouTube error lista: {enlace}")
                return False, "❌ No se pudo leer la lista | Probá actualizar yt-dlp"

            escribir_error(f"YouTube error: {enlace} | {str(e)[:150]}")
            if intentos < max_intentos:
                time.sleep(5 * intentos)
                continue
            return False, f"❌ Fallo final: {str(e)[:70]}"

    return False, "❌ Se agotaron los intentos de descarga"
