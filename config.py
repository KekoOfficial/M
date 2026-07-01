import os
from datetime import datetime

# ─────────────────────────────────────────────────────
# 📁 RUTAS DE ALMACENAMIENTO (Termux / Android)
# Accesibles directamente desde la galería del celular
# ─────────────────────────────────────────────────────
CARPETA_RAIZ       = "/data/data/com.termux/files/home/storage/shared/DescargadorMultiRed"
CARPETA_MUSICA     = os.path.join(CARPETA_RAIZ, "Musica")
CARPETA_TIKTOK     = os.path.join(CARPETA_RAIZ, "TikTok")
CARPETA_INSTAGRAM  = os.path.join(CARPETA_RAIZ, "Instagram")
CARPETA_FACEBOOK   = os.path.join(CARPETA_RAIZ, "Facebook")
CARPETA_TEMPORAL   = os.path.join(CARPETA_RAIZ, "Temporal")

# ─────────────────────────────────────────────────────
# 📄 ARCHIVOS DE SOPORTE Y REGISTROS
# ─────────────────────────────────────────────────────
ARCHIVO_COOKIES    = os.path.join(os.path.dirname(__file__), "cookies_instagram.txt")
ARCHIVO_ERRORES    = os.path.join(CARPETA_RAIZ, "errores.log")
ARCHIVO_ESTADO     = os.path.join(CARPETA_RAIZ, "estado_descargas.txt")
ARCHIVO_ESTADISTICAS = os.path.join(CARPETA_RAIZ, "estadisticas.txt")

# ─────────────────────────────────────────────────────
# ⚙️ CONFIGURACIÓN GENERAL AVANZADA
# ─────────────────────────────────────────────────────
# Rendimiento y límites
MAX_CONEXIONES     = 8               # Menor = menos bloqueos
MAX_INTENTOS       = 3               # Reintentos generales
RETRIES_DESCARGA   = 30              # Reintentos por fragmento
ESPERA_ENTRE_PET   = 3               # Segundos entre descargas
ESPERA_403         = 15              # Espera si hay error 403
MAX_ESPERA         = 20              # Máximo tiempo de espera

# Calidad de salida
CALIDAD_MP3        = "320"           # Máxima calidad MP3
CALIDAD_MP4        = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
FORMATO_VIDEO      = "mp4"
FORMATO_AUDIO      = "mp3"

# Región y seguridad
PAIS_GEOBYPASS     = "PY"            # Paraguay
IDIOMA_PREFERIDO   = "es-PY,es;q=0.9,en;q=0.8"

# Opciones extra
GUARDAR_TEMPORAL   = False           # Eliminar archivos intermedios
INCORPORAR_METADATOS = True          # Guardar título, artista, etc.
INCORPORAR_MINIATURA = True          # Agregar portada al MP3
SALTAR_ERRORES_LISTAS = True         # No detenerse si falla un elemento

# ─────────────────────────────────────────────────────
# 📊 VARIABLES GLOBALES DE CONTROL
# ─────────────────────────────────────────────────────
contador_total_descargas = 0
contador_exitosas        = 0
contador_errores         = 0
contador_duplicados      = 0
hora_inicio              = datetime.now()

# ─────────────────────────────────────────────────────
# 🚀 CREACIÓN AUTOMÁTICA DE CARPETAS
# ─────────────────────────────────────────────────────
carpetas = [
    CARPETA_RAIZ,
    CARPETA_MUSICA,
    CARPETA_TIKTOK,
    CARPETA_INSTAGRAM,
    CARPETA_FACEBOOK,
    CARPETA_TEMPORAL
]

for carpeta in carpetas:
    try:
        os.makedirs(carpeta, exist_ok=True)
        # Permisos de lectura/escritura para Termux
        os.chmod(carpeta, 0o755)
    except Exception as e:
        print(f"⚠️ No se pudo configurar la carpeta {carpeta}: {str(e)[:50]}")

# ─────────────────────────────────────────────────────
# ✅ VERIFICACIÓN FINAL
# ─────────────────────────────────────────────────────
if __name__ == "__main__":
    print("✅ Configuración cargada correctamente")
    print(f"📂 Carpeta principal: {CARPETA_RAIZ}")
    print(f"🕒 Inicio: {hora_inicio.strftime('%d/%m/%Y %H:%M:%S')}")
