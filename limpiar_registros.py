import os

ARCHIVO_ESTADO = "estado_descarga.txt"

def limpiar():
    try:
        if os.path.exists(ARCHIVO_ESTADO):
            os.remove(ARCHIVO_ESTADO)
            print("✅ Archivo de estado borrado")
        else:
            print("ℹ️ No hay archivos temporales")
        print("✅ Limpieza finalizada")
    except Exception as e:
        print(f"❌ Error al limpiar: {e}")

if __name__ == "__main__":
    limpiar()
