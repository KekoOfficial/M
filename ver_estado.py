import time

ARCHIVO_ESTADO = "estado_descarga.txt"

def ver_estado():
    while True:
        try:
            print("\n" + "=" * 50)
            with open(ARCHIVO_ESTADO, "r", encoding="utf-8") as f:
                contenido = f.read().strip()
                if contenido:
                    print(contenido)
                else:
                    print("⌛ Esperando información...")
            print("=" * 50)
            print("🔄 Actualizando cada 2 segundos | Ctrl+C para salir")
            time.sleep(2)
        except KeyboardInterrupt:
            print("\n👋 Cerrando monitor...")
            break
        except:
            print("⚠️ No se pudo leer el estado")
            time.sleep(2)

if __name__ == "__main__":
    ver_estado()
