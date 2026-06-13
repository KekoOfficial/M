# 🎵 Descargador de Medios
Sistema rápido para descargar música y videos en Termux, organizado y sin duplicados.

## ✅ Características
- Descarga música de YouTube en MP3 320kbps
- Descarga videos de TikTok
- Evita archivos duplicados
- Actualiza automáticamente las carpetas para que aparezcan en Android
- Fácil de configurar y ampliar

## 🚀 Instalación en Termux
```bash
pkg update && pkg upgrade -y
pkg install python ffmpeg termux-api git -y
pip install -r requirements.txt
termux-setup-storage
