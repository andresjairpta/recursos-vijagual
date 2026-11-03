#!/usr/bin/env python3
"""
Construye el sitio público de recursos del CER Vijagual (GitHub Pages).

Cada archivo de _paginas/ es un fragmento HTML cuya primera línea es
    <!-- titulo: Nombre de la página | descripcion: una frase -->
y se envuelve con el encabezado institucional (escudo, Secretaría de Educación
de Antioquia, resoluciones, DANE/NIT, Carepa y el lema). El escudo va incrustado
en base64 para que cada página sea un solo archivo que funciona sin señal una
vez abierto. La salida conserva la ruta relativa: _paginas/x/y.html -> x/y.html.

Uso:  python3 _plantilla/construir.py
"""
from __future__ import annotations

import base64
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PAGINAS = RAIZ / "_paginas"
ESCUDO = base64.b64encode((RAIZ / "assets" / "escudo-200.png").read_bytes()).decode()

ENCABEZADO = f"""<header class="inst">
  <img class="escudo" alt="Escudo del Centro Educativo Rural Vijagual" src="data:image/png;base64,{ESCUDO}">
  <div class="inst-texto">
    <p class="sec">SECRETARIA DE EDUCACIÓN DE ANTIOQUIA</p>
    <p class="cer">CENTRO EDUCATIVO RURAL VIJAGUAL</p>
    <p class="res">Aprobado mediante las Resoluciones Departamentales N° 09194 del 19 de mayo de 2008, N° 0094782 del 26 de mayo de 2010, y N° S127203 del 06 de octubre de 2014.</p>
    <p class="res">DANE N° 205147000058 · NIT 811019113-1</p>
    <p class="res">CAREPA - ANTIOQUIA</p>
    <p class="lema">“Formando líderes integrales, transformando comunidades”</p>
  </div>
</header>"""

ENCABEZADO_COMPACTO = f"""<header class="inst compacto">
  <img class="escudo" alt="Escudo del Centro Educativo Rural Vijagual" src="data:image/png;base64,{ESCUDO}">
  <div class="inst-texto">
    <p class="cer">CENTRO EDUCATIVO RURAL VIJAGUAL · <span class="sec">Secretaria de Educación de Antioquia</span></p>
    <p class="res">Resoluciones Departamentales N° 09194 de 2008, N° 0094782 de 2010 y N° S127203 de 2014 · DANE N° 205147000058 · NIT 811019113-1 · Carepa - Antioquia</p>
    <p class="lema">“Formando líderes integrales, transformando comunidades”</p>
  </div>
</header>"""

ESTILO_TV = """
html{font-size:clamp(17px,1.55vw,34px)}
.inst.compacto{padding:6px 16px;gap:12px}
.inst.compacto .escudo{width:3.2rem}
.inst.compacto .cer{font-size:.95rem}
.inst.compacto .sec{font-weight:400;color:var(--suave)}
.inst.compacto .res{font-size:.55rem}
.inst.compacto .lema{font-size:.75rem}
main{max-width:none;padding:12px 2.5vw 24px}
"""

ESTILO = """
:root{--tinta:#1d2b22;--suave:#5b6b60;--verde:#1f6b3a;--verde-claro:#e6f2ea;--amarillo:#f2c230;--rojo:#c0392b;--fondo:#fbfaf6;--tarjeta:#ffffff;--borde:#d9dfd6}
*{box-sizing:border-box}
body{margin:0;background:var(--fondo);color:var(--tinta);font-family:"Century Gothic","Avenir Next","Segoe UI",system-ui,sans-serif;line-height:1.5}
.inst{display:flex;gap:14px;align-items:center;justify-content:center;padding:14px 16px;border-bottom:4px solid var(--verde);background:#fff;text-align:center}
.escudo{width:78px;height:auto;flex:none}
.inst-texto p{margin:0}
.sec{font-weight:700;font-size:.82rem}
.cer{font-weight:800;font-size:1.05rem;color:var(--verde);letter-spacing:.02em}
.res{font-size:.68rem;color:var(--suave)}
.lema{font-style:italic;font-family:Georgia,"Times New Roman",serif;font-size:.92rem;margin-top:3px!important}
main{max-width:860px;margin:0 auto;padding:18px 16px 40px}
h1{font-size:1.45rem;margin:.4em 0 .2em;color:var(--verde)}
h2{font-size:1.15rem;margin:1.4em 0 .4em}
.sub{color:var(--suave);margin-top:0}
.tarjeta{background:var(--tarjeta);border:1px solid var(--borde);border-radius:12px;padding:14px 16px;margin:10px 0}
a{color:var(--verde)}
.nota{font-size:.85rem;color:var(--suave)}
button,.boton{font:inherit;border:0;border-radius:10px;padding:10px 14px;background:var(--verde);color:#fff;cursor:pointer;text-decoration:none;display:inline-block}
button.sec2{background:var(--verde-claro);color:var(--verde)}
input,select{font:inherit;padding:8px 10px;border:1px solid var(--borde);border-radius:8px;width:100%}
footer{text-align:center;font-size:.75rem;color:var(--suave);padding:16px}
@media (max-width:560px){.inst{flex-direction:column;gap:6px}.escudo{width:64px}}
@media print{.no-imprimir{display:none!important}body{background:#fff}}
"""


def construir() -> None:
    for fuente in sorted(PAGINAS.rglob("*.html")):
        texto = fuente.read_text(encoding="utf-8")
        m = re.match(r"<!--\s*titulo:\s*(.*?)\s*\|\s*descripcion:\s*(.*?)\s*(?:\|\s*modo:\s*(tv))?\s*-->\s*", texto)
        if not m:
            raise SystemExit(f"Falta la línea de título en {fuente}")
        titulo, descripcion, modo = m.group(1), m.group(2), m.group(3)
        cuerpo = texto[m.end():]
        encabezado = ENCABEZADO_COMPACTO if modo == "tv" else ENCABEZADO
        estilo = ESTILO + (ESTILO_TV if modo == "tv" else "")
        pagina = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo} · CER Vijagual</title>
<meta name="description" content="{descripcion}">
<style>{estilo}</style>
</head>
<body>
{encabezado}
<main>
{cuerpo}
</main>
<footer>Centro Educativo Rural Vijagual · Vereda Vijagual, Carepa (Antioquia) · Recurso educativo de uso libre en el aula</footer>
</body>
</html>
"""
        destino = RAIZ / fuente.relative_to(PAGINAS)
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(pagina, encoding="utf-8")
        print("construida:", destino.relative_to(RAIZ))


if __name__ == "__main__":
    construir()
