import os
from config import CARPETA_MUSICA, CARPETA_TIKTOK, ARCHIVO_ESTADO

def escribir_estado(datos):
    """Guarda el estado actual en archivo de texto"""
    try:
        with open(ARCHIVO_ESTADO, "w", encoding="utf-8") as f:
            f.write(datos)
    except Exception as e:
        print(f"⚠️ Error al escribir estado: {e}")

def actualizar_carpeta(ruta):
    """Actualiza la carpeta para que Android detecte los archivos nuevos"""
    try:
        os.system(f"termux-media-scan -r {ruta} > /dev/null 2>&1")
        print(f"🔄 Carpeta actualizada: {ruta}")
    except Exception as e:
        print(f"⚠️ No se pudo actualizar carpeta: {e}")

def crear_carpetas():
    """Crea las carpetas si no existen"""
    os.makedirs(CARPETA_MUSICA, exist_ok=True)
    os.makedirs(CARPETA_TIKTOK, exist_ok=True)
