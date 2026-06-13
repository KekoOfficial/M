import threading
import queue
from config import CARPETA_MUSICA, CARPETA_TIKTOK
from utils import escribir_estado, crear_carpetas, actualizar_carpeta
from archivos import obtener_datos, borrar_duplicados
from descargas import descargar

cola = queue.Queue()

def procesar_cola():
    """Procesa cada enlace en la cola de descargas"""
    numero = 1
    while True:
        enlace = cola.get()
        if enlace is None:
            datos = obtener_datos()
            texto_final = f"""
✅ TODAS LAS DESCARGAS FINALIZADAS ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📂 Total archivos: {datos['total']}
🎵 Música: {datos['musica']} | 📹 TikTok: {datos['tiktok']}
💾 Tamaño total: {datos['tam_total']} MB
🗑️ Duplicados borrados: {datos['duplicados']}
🔄 Carpetas actualizadas ✅
"""
            escribir_estado(texto_final)
            break

        estado, mensaje = descargar(enlace)
        print(f"📌 N° {numero} → {mensaje}")
        numero += 1
        cola.task_done()

def iniciar():
    """Inicializa todo el sistema"""
    crear_carpetas()
    borrar_duplicados()
    actualizar_carpeta(CARPETA_MUSICA)
    actualizar_carpeta(CARPETA_TIKTOK)
    escribir_estado("💤 Sistema listo | Esperando enlaces...")

    hilo = threading.Thread(target=procesar_cola, daemon=True)
    hilo.start()

    print("\n" + "=" * 60)
    print("🎵 DESCARGADOR MEDIA | LISTO PARA USAR ⚡")
    print("🔗 Soporte: YouTube, YouTube Music, TikTok")
    print("🚫 No repite archivos | 🗑️ Borra duplicados")
    print("=" * 60 + "\n")

    while True:
        enlace = input("🔗 Pegá enlace o escribí 'fin' para terminar:\n> ").strip()
        if enlace.lower() == "fin":
            print("\n👋 Finalizando... espere un momento")
            cola.join()
            cola.put(None)
            break
        if not enlace:
            print("⚠️ Ingresá un enlace válido")
            continue
        cola.put(enlace)
        print(f"📥 Agregado | Pendientes: {cola.qsize()}\n")

if __name__ == "__main__":
    iniciar()
