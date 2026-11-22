#!/usr/bin/env python3
"""Descubridor sin Make: lista los últimos vídeos de cuentas de TikTok / YouTube Shorts con sus
visualizaciones y marca como virales los que superan `umbral` veces la mediana de su creador.

Uso:
  python3 generador/descubrir.py URL_PERFIL [URL_PERFIL ...] [--n 30] [--umbral 3] [--salida datos/ronda.json]
  python3 generador/descubrir.py --bajar URL_VIDEO carpeta/   # descarga un vídeo (también reels sueltos de Instagram)

Ejemplos de perfil: https://www.tiktok.com/@usuario   https://www.youtube.com/@canal/shorts
Instagram no deja listar perfiles sin sesión, pero sí descargar un reel suelto por su URL.
Solo para analizar la estructura: nunca resubir ni copiar el vídeo, la música o el texto.
"""
import json, statistics, subprocess, sys, os, datetime


def listar(url, n):
    cmd = ["yt-dlp", "-q", "--no-warnings", "--flat-playlist", "--playlist-end", str(n),
           "--print", "%(.{id,url,webpage_url,title,view_count,like_count,comment_count,duration,timestamp,upload_date})j", url]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    vids = []
    for linea in r.stdout.splitlines():
        try:
            vids.append(json.loads(linea))
        except Exception:
            pass
    return vids, r.stderr.strip()[-300:]


def main(argv):
    if argv[:1] == ["--bajar"]:
        url, carpeta = argv[1], argv[2]
        os.makedirs(carpeta, exist_ok=True)
        import time
        for intento, espera in enumerate([0, 60, 180]):
            time.sleep(espera)
            r = subprocess.run(["yt-dlp", "-q", "--no-warnings", "-o", os.path.join(carpeta, "video.%(ext)s"),
                                "--merge-output-format", "mp4", "--write-info-json", url],
                               capture_output=True, text=True, timeout=300)
            if r.returncode == 0:
                print("ok"); return
            if "429" not in r.stderr:
                break
            print(f"Instagram limita (429), espero y reintento ({intento + 1}/3)")
        print(r.stderr.strip()[-300:]); sys.exit(1)
    n, umbral, salida, perfiles = 30, 3.0, None, []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--n": n = int(argv[i + 1]); i += 2; continue
        if a == "--umbral": umbral = float(argv[i + 1]); i += 2; continue
        if a == "--salida": salida = argv[i + 1]; i += 2; continue
        perfiles.append(a); i += 1
    ronda = {"fecha": datetime.date.today().isoformat(), "umbral": umbral, "cuentas": []}
    for p in perfiles:
        vids, err = listar(p, n)
        vistas = [v["view_count"] for v in vids if isinstance(v.get("view_count"), int) and v["view_count"] > 0]
        med = statistics.median(vistas) if vistas else None
        for v in vids:
            vc = v.get("view_count") or 0
            v["veces_mediana"] = round(vc / med, 2) if med else None
            v["viral"] = bool(med and vc >= umbral * med)
        virales = sorted([v for v in vids if v["viral"]], key=lambda v: -(v["veces_mediana"] or 0))
        ronda["cuentas"].append({"perfil": p, "revisados": len(vids), "mediana_vistas": med,
                                 "virales": virales, "error": err if not vids else ""})
        print(f"{p}: {len(vids)} revisados, mediana {med}, {len(virales)} virales" + (f"  ERROR: {err}" if not vids else ""))
        for v in virales[:5]:
            print(f"   x{v['veces_mediana']}  {v.get('view_count')} vistas  {v.get('webpage_url') or v.get('url')}  {str(v.get('title'))[:60]}")
    ronda["total_revisados"] = sum(c["revisados"] for c in ronda["cuentas"])
    ronda["total_virales"] = sum(len(c["virales"]) for c in ronda["cuentas"])
    if salida:
        os.makedirs(os.path.dirname(salida) or ".", exist_ok=True)
        json.dump(ronda, open(salida, "w"), ensure_ascii=False, indent=1)
    print(f"TOTAL: {ronda['total_revisados']} revisados, {ronda['total_virales']} virales")


if __name__ == "__main__":
    main(sys.argv[1:])
