import threading, queue
from config import *
from utils import escribir_estado, actualizar_carpeta
from archivos import obtener_datos, borrar_duplicados
from descargas import descargar

cola = queue.Queue()

def procesar_cola():
    n = 1
    while True:
        enlace = cola.get()
        if enlace is None:
            datos = obtener_datos()
            escribir_estado(f"""✅ FINALIZADO
Total: {datos['total']} | MP3: {datos['mp3']} | MP4: {datos['mp4']}
Tamaño: {datos['tam_total']} MB | Duplicados: {datos['duplicados']}""")
            break
        ok, msg = descargar(enlace)
        print(f"📌 {n:02d} → {msg}")
        n += 1
        cola.task_done()

def iniciar():
    borrar_duplicados()
    escribir_estado("💤 Sistema listo")
    threading.Thread(target=procesar_cola, daemon=True).start()
    print("\n" + "=" * 60)
    print("🎵 YouTube → MP3 320kbps")
    print("🎬 15 Redes Sociales → MP4 HD")
    print("🔹 Facebook • WhatsApp • Instagram • TikTok • X")
    print("🔹 Telegram • LinkedIn • Discord • Snapchat • Pinterest")
    print("🔹 Threads • Reddit • Messenger • Bigo Live • Otros")
    print("=" * 60 + "\n")
    while True:
        enlace = input("🔗 Enlace o 'fin' para salir:\n> ").strip()
        if enlace.lower() == "fin":
            print("\n⏳ Terminando descargas pendientes...")
            cola.join()
            cola.put(None)
            break
        if enlace:
            cola.put(enlace)
            print(f"📥 Agregado | En cola: {cola.qsize()}\n")

if __name__ == "__main__":
    iniciar()
