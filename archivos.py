import os, glob
from config import *

def contar_archivos(carpeta, ext):
    arch = glob.glob(f"{carpeta}/**/*.{ext}", recursive=True)
    tam = sum(os.path.getsize(f) for f in arch if os.path.isfile(f))/(1024*1024) if arch else 0
    return len(arch), round(tam, 2)

def obtener_datos():
    mp3_n, mp3_t = contar_archivos(CARPETA_MUSICA, "mp3")
    fb_n, fb_t = contar_archivos(CARPETA_FACEBOOK, "mp4")
    wa_n, wa_t = contar_archivos(CARPETA_WHATSAPP, "mp4")
    ig_n, ig_t = contar_archivos(CARPETA_INSTAGRAM, "mp4")
    tt_n, tt_t = contar_archivos(CARPETA_TIKTOK, "mp4")
    x_n, x_t = contar_archivos(CARPETA_X, "mp4")
    tg_n, tg_t = contar_archivos(CARPETA_TELEGRAM, "mp4")
    li_n, li_t = contar_archivos(CARPETA_LINKEDIN, "mp4")
    dc_n, dc_t = contar_archivos(CARPETA_DISCORD, "mp4")
    sc_n, sc_t = contar_archivos(CARPETA_SNAPCHAT, "mp4")
    pi_n, pi_t = contar_archivos(CARPETA_PINTEREST, "mp4")
    th_n, th_t = contar_archivos(CARPETA_THREADS, "mp4")
    rd_n, rd_t = contar_archivos(CARPETA_REDDIT, "mp4")
    ms_n, ms_t = contar_archivos(CARPETA_MESSENGER, "mp4")
    bl_n, bl_t = contar_archivos(CARPETA_BIGOLIVE, "mp4")
    ot_n, ot_t = contar_archivos(CARPETA_OTROS, "mp4")

    total = mp3_n+fb_n+wa_n+ig_n+tt_n+x_n+tg_n+li_n+dc_n+sc_n+pi_n+th_n+rd_n+ms_n+bl_n+ot_n
    total_mb = round(mp3_t+fb_t+wa_t+ig_t+tt_t+x_t+tg_t+li_t+dc_t+sc_t+pi_t+th_t+rd_t+ms_t+bl_t+ot_t, 2)

    return {
        "total": total, "mp3": mp3_n, "mp4": total-mp3_n,
        "tam_total": total_mb, "duplicados": contador_duplicados
    }

def borrar_duplicados():
    global contador_duplicados
    arch = glob.glob(f"{CARPETA_MUSICA}/**/*.mp3", recursive=True)
    vistos = set()
    borrados = 0
    for ruta in arch:
        nom = os.path.basename(ruta)
        if nom in vistos:
            try: os.remove(ruta); borrados +=1
            except: pass
        else: vistos.add(nom)
    contador_duplicados += borrados
    if borrados: print(f"♻️ Duplicados eliminados: {borrados}")
