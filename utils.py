import os
from config import ARCHIVO_COOKIES

def actualizar_carpeta(ruta):
    """Actualiza permisos de la carpeta"""
    if os.path.exists(ruta):
        try:
            os.chmod(ruta, 0o755)
        except:
            pass

def tiene_cookies():
    """Verifica si existe el archivo de cookies para Instagram"""
    return os.path.exists(ARCHIVO_COOKIES)
