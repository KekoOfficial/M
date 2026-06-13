import os
import glob
from config import CARPETA_MUSICA, CARPETA_TIKTOK, contador_duplicados

def obtener_datos():
    """Devuelve estadísticas de archivos guardados"""
    archivos_mp3 = glob.glob(f"{CARPETA_MUSICA}/**/*.mp3", recursive=True)
    archivos_mp4 = glob.glob(f"{CARPETA_TIKTOK}/*.mp4", recursive=True)

    tam_musica = sum(os.path.getsize(f) for f in archivos_mp3) / (1024 * 1024) if archivos_mp3 else 0
    tam_tiktok = sum(os.path.getsize(f) for f in archivos_mp4) / (1024 * 1024) if archivos_mp4 else 0

    return {
        "total": len(archivos_mp3) + len(archivos_mp4),
        "musica": len(archivos_mp3),
        "tiktok": len(archivos_mp4),
        "tam_musica": round(tam_musica, 2),
        "tam_tiktok": round(tam_tiktok, 2),
        "tam_total": round(tam_musica + tam_tiktok, 2),
        "duplicados": contador_duplicados
    }

def borrar_duplicados():
    """Borra archivos con el mismo nombre en la carpeta de música"""
    global contador_duplicados
    archivos = glob.glob(f"{CARPETA_MUSICA}/**/*.mp3", recursive=True)
    nombres_vistos = set()

    for ruta in archivos:
        nombre = os.path.basename(ruta)
        if nombre in nombres_vistos:
            try:
                os.remove(ruta)
                contador_duplicados += 1
            except:
                pass
        else:
            nombres_vistos.add(nombre)
