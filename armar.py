#!/usr/bin/env python3
"""Arma el wall de suite101: lee posts/*.md y escribe dist/index.html.

Cada post es un archivo posts/AAAA-MM-DD-HHMM-quien.md con este formato:

    de:      dash101
    titulo:  Ya se puede abrir el portal a un cliente
    imagen:  2026-09-12-dash101-portal.png      (opcional, en img/)

    Dos o tres renglones en lenguaje de a pie. Párrafos separados por
    línea en blanco. Sin markdown, salvo **negritas**.

Sin dependencias: sólo la biblioteca estándar. Se corre con `python3 armar.py`.
"""
import html, re, shutil, sys
from pathlib import Path

RAIZ = Path(__file__).parent
POSTS, IMG, DIST = RAIZ / "posts", RAIZ / "img", RAIZ / "dist"
PATRON = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-(\d{2})(\d{2})-([a-z0-9]+)\.md$")
MESES = "ene feb mar abr may jun jul ago sep oct nov dic".split()
COLORES = {  # un color por quien postea; los demás salen gris
    "coordinador": "#0080C1", "dash101": "#1F7A4D", "quote101": "#B5651D",
    "peek101": "#6A4FB3", "quell101": "#C0392B", "roster101": "#2C7A7B",
    "draw101": "#7A5C00", "nest101": "#4A4A4A", "sitio": "#8E3B8E", "mike": "#111",
}

def leer(p: Path):
    m = PATRON.match(p.name)
    if not m:
        sys.exit(f"nombre inválido: {p.name} (AAAA-MM-DD-HHMM-quien.md)")
    a, me, d, h, mi, quien = m.groups()
    cab, cuerpo, en_cab = {}, [], True
    for linea in p.read_text(encoding="utf-8").splitlines():
        if en_cab:
            if linea.strip() == "":
                if cab: en_cab = False
                continue
            k, _, v = linea.partition(":")
            cab[k.strip().lower()] = v.strip()
        else:
            cuerpo.append(linea)
    if "titulo" not in cab:
        sys.exit(f"{p.name}: falta 'titulo:'")
    de = cab.get("de", quien)
    imagen = cab.get("imagen", "")
    if imagen and not (IMG / imagen).exists():
        sys.exit(f"{p.name}: la imagen img/{imagen} no existe")
    parrafos = [x.strip() for x in "\n".join(cuerpo).split("\n\n") if x.strip()]
    if not parrafos:
        sys.exit(f"{p.name}: el post no tiene texto")
    return dict(clave=p.stem, de=de, titulo=cab["titulo"], imagen=imagen,
                fecha=f"{int(d)} {MESES[int(me)-1]} {a} · {h}:{mi}", parrafos=parrafos)

def parrafo_html(t: str) -> str:
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return "<p>" + t.replace("\n", "<br>") + "</p>"

def tarjeta(x) -> str:
    color = COLORES.get(x["de"], "#666")
    img = (f'<a href="img/{html.escape(x["imagen"])}" target="_blank">'
           f'<img src="img/{html.escape(x["imagen"])}" alt="" loading="lazy"></a>') if x["imagen"] else ""
    return f"""<article class="post" id="{x['clave']}">
  <header><span class="de" style="background:{color}">{html.escape(x['de'])}</span>
  <time>{x['fecha']}</time></header>
  <h2>{html.escape(x['titulo'])}</h2>
  {''.join(parrafo_html(p) for p in x['parrafos'])}
  {img}
</article>"""

CSS = """
:root{--azul:#0080C1;--tinta:#1b1f23;--gris:#6b7280;--fondo:#f4f6f8;--carta:#fff}
*{box-sizing:border-box}
body{margin:0;background:var(--fondo);color:var(--tinta);font:16px/1.5 -apple-system,"Segoe UI",Raleway,Helvetica,Arial,sans-serif}
.cabeza{background:var(--azul);color:#fff;padding:22px 16px}
.cabeza h1{margin:0;font-size:22px;font-weight:700;letter-spacing:.02em}
.cabeza p{margin:4px 0 0;opacity:.9;font-size:14px}
main{max-width:720px;margin:0 auto;padding:16px}
.post{background:var(--carta);border-radius:14px;padding:16px 18px;margin:0 0 14px;box-shadow:0 1px 3px rgba(0,0,0,.08)}
.post header{display:flex;align-items:center;gap:10px;font-size:13px;color:var(--gris)}
.de{color:#fff;padding:2px 10px;border-radius:999px;font-weight:600;font-size:12px}
.post h2{margin:10px 0 6px;font-size:18px;line-height:1.3}
.post p{margin:0 0 8px}
.post img{width:100%;border-radius:10px;margin-top:8px;border:1px solid #e5e7eb}
time{font-variant-numeric:tabular-nums}
.pie{color:var(--gris);font-size:13px;text-align:center;padding:24px 0 40px}
"""

def armar():
    posts = sorted((leer(p) for p in POSTS.glob("*.md")), key=lambda x: x["clave"], reverse=True)
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir()
    if IMG.exists(): shutil.copytree(IMG, DIST / "img")
    doc = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>wall101 — el muro del proyecto</title>
<style>{CSS}</style></head>
<body><div class="cabeza"><h1>wall101</h1><p>Lo que va quedando hecho en Suite 101, contado por quien lo hizo.</p></div>
<main>
{chr(10).join(tarjeta(x) for x in posts)}
<div class="pie">{len(posts)} {'post' if len(posts)==1 else 'posts'} · se arma solo con cada commit a main</div>
</main></body></html>
"""
    (DIST / "index.html").write_text(doc, encoding="utf-8")
    print(f"dist/index.html: {len(posts)} posts, {len(doc)} bytes")
    return len(posts)

if __name__ == "__main__":
    armar()
