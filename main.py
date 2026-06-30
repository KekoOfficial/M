import threading
import queue
from youtube import descargar_youtube
from tiktok import descargar_tiktok
from instagram import descargar_instagram
from facebook import descargar_facebook

cola = queue.Queue()

def detectar_plataforma(enlace):
    enlace = enlace.lower().strip()
    if "youtube.com" in enlace or "youtu.be" in enlace:
        return descargar_youtube
    elif "tiktok.com" in enlace:
        return descargar_tiktok
    elif "instagram.com" in enlace or "instagr.am" in enlace:
        return descargar_instagram
    elif "facebook.com" in enlace or "fb.watch" in enlace:
        return descargar_facebook
    else:
        return None

def procesar_cola():
    numero = 1
    while True:
        enlace = cola.get()
        if enlace is None:
            print("\n✅ Todas las descargas finalizadas\n")
            break

        funcion = detectar_plataforma(enlace)
        if not funcion:
            print(f"📌 {numero:02d} → ❌ Enlace no compatible")
            numero += 1
            cola.task_done()
            continue

        exito, mensaje = funcion(enlace)
        print(f"📌 {numero:02d} → {mensaje}")
        numero += 1
        cola.task_done()

def iniciar():
    hilo = threading.Thread(target=procesar_cola, daemon=True)
    hilo.start()

    print("\n" + "=" * 55)
    print("📥 DESCARGADOR MULTIRED")
    print("🎵 YouTube → MP3 | 🎬 TikTok/IG/FB → MP4")
    print("=" * 55 + "\n")

    while True:
        enlace = input("🔗 Pegá enlace o escribí 'fin' para salir:\n> ").strip()
        if enlace.lower() == "fin":
            print("\n⏳ Esperando que terminen las descargas...")
            cola.join()
            cola.put(None)
            break
        if not enlace:
            print("⚠️ Ingresá un enlace válido\n")
            continue
        cola.put(enlace)
        print(f"📥 Agregado | Pendientes: {cola.qsize()}\n")

if __name__ == "__main__":
    iniciar()
