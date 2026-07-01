import yt_dlp
import os
import time
import random
import re
import requests
from urllib.parse import urlencode
from config import (
    CARPETA_INSTAGRAM, CALIDAD_MP4, MAX_CONEXIONES,
    REINTENTOS, ESPERA_ENTRE_PET, PAIS_GEOBYPASS, ARCHIVO_ERRORES
)
from utils import actualizar_carpeta, escribir_error, limpiar_nombre

# ─────────────────────────────────────────────────────────────
# ⚙️ CONFIGURACIÓN: MOTOR = sssinstagram.com/es
# ─────────────────────────────────────────────────────────────
MOTOR_URL = "https://sssinstagram.com/es"
API_ENDPOINT = "https://sssinstagram.com/api/instagram"

USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/132.0.0.0 Safari/537.36"
]

# Opciones finales de descarga MP4
OPCIONES_DESCARGA = {
    "format": "best[ext=mp4]/best",
    "outtmpl": f"{CARPETA_INSTAGRAM}/%(id)s_{limpiar_nombre('%(title)s')}.%(ext)s",
    "noplaylist": True,
    "quiet": False,
    "no_warnings": False,
    "overwrites": False,
    "retries": REINTENTOS,
    "fragment_retries": REINTENTOS,
    "sleep_interval": ESPERA_ENTRE_PET,
    "http_headers": {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": MOTOR_URL,
        "Origin": "https://sssinstagram.com"
    }
}

# ─────────────────────────────────────────────────────────────
# 🛠️ FUNCIÓN: Extraer enlace directo vía sssinstagram.com
# ─────────────────────────────────────────────────────────────
def obtener_enlace_directo(enlace_ig: str) -> tuple[bool, str, dict]:
    """Consulta el servicio sssinstagram para obtener el enlace MP4"""
    try:
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Referer": MOTOR_URL,
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        payload = urlencode({"url": enlace_ig.strip()})

        resp = requests.post(
            API_ENDPOINT,
            data=payload,
            headers=headers,
            timeout=15
        )
        resp.raise_for_status()
        datos = resp.json()

        if datos.get("success") and datos.get("video"):
            enlace_mp4 = datos["video"].get("url") or datos["video"].get("download")
            titulo = datos.get("title", "Instagram_" + datos.get("id", "desconocido"))
            return True, enlace_mp4, {"title": titulo, "id": datos.get("id", "")}

        escribir_error(f"SSSInstagram: No devolvió enlace válido | {enlace_ig}")
        return False, "", {}

    except Exception as e:
        escribir_error(f"SSSInstagram Error: {enlace_ig} | {str(e)[:80]}")
        return False, "", {}

# ─────────────────────────────────────────────────────────────
# 📥 FUNCIÓN PRINCIPAL
# ─────────────────────────────────────────────────────────────
def descargar_instagram(enlace: str) -> tuple[bool, str]:
    intentos = 0
    max_intentos = 3
    enlace = enlace.strip()

    # Validar formato Instagram
    if not re.match(r"^https?://(www\.)?instagram\.com/(reel|p|tv)/", enlace):
        return False, "❌ Enlace no es de Instagram válido"

    while intentos < max_intentos:
        try:
            print(f"📸 Procesando Instagram vía SSSInstagram: {enlace[:65]}...")

            ok, enlace_mp4, info = obtener_enlace_directo(enlace)
            if not ok or not enlace_mp4:
                intentos += 1
                time.sleep(3 * intentos)
                continue

            # Ajustar nombre en opciones
            opciones = OPCIONES_DESCARGA.copy()
            opciones["outtmpl"] = opciones["outtmpl"] % info

            # Descargar con yt-dlp desde el enlace directo
            with yt_dlp.YoutubeDL(opciones) as ydl:
                ydl.download([enlace_mp4])

            actualizar_carpeta(CARPETA_INSTAGRAM)
            return True, f"✅ Instagram descargado: {limpiar_nombre(info.get('title', ''))[:50]}"

        except Exception as e:
            intentos += 1
            error = str(e).lower()

            if "already exists" in error:
                return False, "⚠️ Ya existe, saltado"

            escribir_error(f"Instagram Fallo: {enlace} | {str(e)[:100]}")
            if intentos < max_intentos:
                time.sleep(4 * intentos)
                continue
            return False, f"❌ Error final: {str(e)[:70]}"

    return False, "❌ Se agotaron los intentos"
