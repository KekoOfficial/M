import os
from config import ARCHIVO_ESTADO

def actualizar_carpeta(ruta):
    if os.path.exists(ruta):
        try: os.chmod(ruta, 0o755)
        except: pass

def escribir_estado(texto):
    try:
        with open(ARCHIVO_ESTADO, "w", encoding="utf-8") as f:
            f.write(texto)
    except: pass
