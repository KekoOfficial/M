import os
import glob
from config import CARPETA_MUSICA, contador_duplicados, contador_total_descargas, contador_exitosas
from utils import limpiar_nombre, escribir_error

def borrar_duplicados():
    """Elimina archivos duplicados por nombre"""
    global contador_duplicados
    try:
        archivos = glob.glob(f"{CARPETA_MUSICA}/**/*.mp3", recursive=True)
        vistos = set()
        borrados = 0

        for ruta in archivos:
            nombre = os.path.basename(ruta).lower()
            if nombre in vistos:
                try:
                    os.remove(ruta)
                    borrados += 1
                except Exception as e:
                    escribir_error(f"No se pudo borrar duplicado {ruta}: {e}")
            else:
                vistos.add(nombre)

        contador_duplicados += borrados
        if borrados > 0:
            print(f"♻️ Eliminados {borrados} archivos duplicados")

    except Exception as e:
        escribir_error(f"Error al buscar duplicados: {e}")

def registrar_descarga(plataforma, info):
    """Actualiza contadores globales"""
    global contador_total_descargas, contador_exitosas
    try:
        contador_total_descargas += 1
        if info and isinstance(info, dict):
            contador_exitosas += 1
    except:
        pass
