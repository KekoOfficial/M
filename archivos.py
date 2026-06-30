import os
import glob
from config import CARPETA_MUSICA, contador_duplicados

def borrar_duplicados():
    """Elimina archivos MP3 repetidos por nombre"""
    global contador_duplicados
    archivos = glob.glob(f"{CARPETA_MUSICA}/**/*.mp3", recursive=True)
    vistos = set()
    borrados = 0

    for ruta in archivos:
        nombre = os.path.basename(ruta)
        if nombre in vistos:
            try:
                os.remove(ruta)
                borrados += 1
            except:
                pass
        else:
            vistos.add(nombre)

    contador_duplicados += borrados
    if borrados > 0:
        print(f"♻️ Eliminados {borrados} archivos duplicados")
