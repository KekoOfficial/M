import os
import time
from datetime import datetime
from config import ARCHIVO_ERRORES, ARCHIVO_ESTADO, ARCHIVO_ESTADISTICAS

# ─────────────────────────────────────────────────────
# 📁 GESTIÓN DE CARPETAS Y ARCHIVOS
# ─────────────────────────────────────────────────────
def actualizar_carpeta(ruta):
    """Actualiza permisos y fechas de carpetas para Termux"""
    try:
        if os.path.exists(ruta):
            os.chmod(ruta, 0o755)
            os.utime(ruta, None)
        else:
            os.makedirs(ruta, exist_ok=True)
    except Exception as e:
        escribir_error(f"No se pudo actualizar carpeta {ruta}: {str(e)}")

def obtener_tamano_formateado(ruta):
    """Devuelve tamaño en KB/MB/GB de forma legible"""
    if not os.path.exists(ruta):
        return "0 B"
    tamano = os.path.getsize(ruta)
    for unidad in ['B', 'KB', 'MB', 'GB']:
        if tamano < 1024:
            return f"{tamano:.2f} {unidad}"
        tamano /= 1024
    return f"{tamano:.2f} TB"

# ─────────────────────────────────────────────────────
# 📝 REGISTROS Y ERRORES
# ─────────────────────────────────────────────────────
def escribir_error(mensaje):
    """Guarda errores con fecha en el archivo de log"""
    try:
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        linea = f"[{fecha}] ❌ {mensaje}\n"
        with open(ARCHIVO_ERRORES, "a", encoding="utf-8") as f:
            f.write(linea)
    except:
        pass

def escribir_estado(mensaje):
    """Guarda mensajes de estado del proceso"""
    try:
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        linea = f"[{fecha}] ℹ️ {mensaje}\n"
        with open(ARCHIVO_ESTADO, "a", encoding="utf-8") as f:
            f.write(linea)
    except:
        pass

def limpiar_registros_antiguos(dias=30):
    """Limpia registros con más de 30 días"""
    try:
        if os.path.exists(ARCHIVO_ERRORES):
            modificado = os.path.getmtime(ARCHIVO_ERRORES)
            if (time.time() - modificado) > (dias * 86400):
                os.remove(ARCHIVO_ERRORES)
    except:
        pass

# ─────────────────────────────────────────────────────
# 🧹 HERRAMIENTAS AUXILIARES
# ─────────────────────────────────────────────────────
def limpiar_nombre(texto):
    """Elimina caracteres no permitidos en nombres de archivos"""
    caracteres_no_permitidos = '<>:"/\\|?*'
    for c in caracteres_no_permitidos:
        texto = texto.replace(c, "_")
    return texto.strip()[:120]

def verificar_permisos(ruta):
    """Comprueba si se puede leer y escribir en la ruta"""
    return os.access(ruta, os.R_OK | os.W_OK)
