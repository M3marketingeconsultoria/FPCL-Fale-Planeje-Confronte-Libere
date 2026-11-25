#!/usr/bin/env python3
"""Auditoria básica de SEO / mobile / performance / acessibilidade em HTML estático.

Uso: python3 audit_html.py <arquivo.html | pasta> [...]
Sai com código 1 se houver ERROS. Sem dependências externas.
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.title = ""
        self._in_title = False
        self.metas = {}      # name/property -> content
        self.links = []      # dicts de <link>
        self.h = []          # níveis de heading em ordem
        self.imgs = []
        self.scripts = []
        self.jsonld = []
        self._in_jsonld = False
        self.tags = {}
        self.labels_for = set()
        self.fields = []
        self.anchors = []
        self._cur_a = None
        self.text_chunks = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags[tag] = self.tags.get(tag, 0) + 1
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.metas[key.lower()] = a.get("content", "")
            if "charset" in a:
                self.metas["charset"] = a["charset"]
        elif tag == "link":
            self.links.append(a)
        elif re.fullmatch(r"h[1-6]", tag):
            self.h.append(int(tag[1]))
        elif tag == "img":
            self.imgs.append(a)
        elif tag == "script":
            self.scripts.append(a)
            if a.get("type") == "application/ld+json":
                self._in_jsonld = True
                self.jsonld.append("")
        elif tag == "label" and a.get("for"):
            self.labels_for.add(a["for"])
        elif tag in ("input", "select", "textarea"):
            if a.get("type") not in ("hidden", "submit", "button", "image", "reset"):
                self.fields.append(a)
        elif tag == "a":
            self._cur_a = {"attrs": a, "text": ""}
            self.anchors.append(self._cur_a)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script":
            self._in_jsonld = False
        elif tag == "a":
            self._cur_a = None

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_jsonld and self.jsonld:
            self.jsonld[-1] += data
        if self._cur_a is not None:
            self._cur_a["text"] += data
        self.text_chunks.append(data)


def audit(path: Path):
    html = path.read_text(encoding="utf-8", errors="replace")
    p = Page()
    p.feed(html)
    errors, warns = [], []
    E, W = errors.append, warns.append
    m = p.metas

    # --- Básico / mobile
    if not p.lang:
        E("<html> sem atributo lang (use lang=\"pt-BR\")")
    if "charset" not in m:
        E("Falta <meta charset=\"utf-8\">")
    vp = m.get("viewport", "")
    if not vp:
        E("Falta <meta name=\"viewport\"> (essencial para mobile)")
    else:
        if "width=device-width" not in vp:
            E("viewport sem width=device-width")
        if re.search(r"user-scalable\s*=\s*(no|0)|maximum-scale\s*=\s*1(\.0)?\b", vp):
            E("viewport bloqueia zoom (user-scalable/maximum-scale)")

    # --- SEO técnico
    t = p.title.strip()
    if not t:
        E("Falta <title>")
    elif not 30 <= len(t) <= 65:
        W(f"<title> com {len(t)} caracteres (ideal 50-60)")
    d = m.get("description", "").strip()
    if not d:
        E("Falta meta description")
    elif not 70 <= len(d) <= 170:
        W(f"meta description com {len(d)} caracteres (ideal 120-160)")
    canon = [l for l in p.links if "canonical" in (l.get("rel") or "").lower()]
    if not canon:
        E("Falta <link rel=\"canonical\">")
    elif not (canon[0].get("href") or "").startswith("http"):
        W("canonical deveria ser URL absoluta")
    robots = m.get("robots", "").lower()
    if "noindex" in robots:
        W("Página com noindex (ok apenas para obrigado/admin/testes)")

    # --- Headings / semântica
    h1 = p.h.count(1)
    if h1 == 0:
        E("Falta <h1>")
    elif h1 > 1:
        E(f"{h1} <h1> na página (use apenas um)")
    for prev, cur in zip(p.h, p.h[1:]):
        if cur - prev > 1:
            W(f"Hierarquia de headings pulou de h{prev} para h{cur}")
            break
    if not p.tags.get("main"):
        W("Falta <main>")
    elif p.tags["main"] > 1:
        W("Mais de um <main>")
    for sem in ("header", "footer"):
        if not p.tags.get(sem):
            W(f"Falta <{sem}>")

    # --- Social
    for k in ("og:title", "og:description", "og:image", "og:url"):
        if not m.get(k):
            W(f"Falta {k} (Open Graph)")
    if not m.get("twitter:card"):
        W("Falta twitter:card")
    if m.get("og:image") and not m["og:image"].startswith("http"):
        W("og:image deveria ser URL absoluta")

    # --- Dados estruturados
    if not p.jsonld:
        W("Sem dados estruturados JSON-LD")
    for i, raw in enumerate(p.jsonld, 1):
        try:
            json.loads(raw)
        except Exception as e:  # noqa: BLE001
            E(f"JSON-LD #{i} inválido: {e}")

    # --- Imagens
    for img in p.imgs:
        src = img.get("src") or img.get("data-src") or "(sem src)"
        if "alt" not in img:
            E(f"<img> sem alt: {src}")
        if not (img.get("width") and img.get("height")):
            W(f"<img> sem width/height (causa CLS): {src}")
    lazy = [i for i in p.imgs if (i.get("loading") or "").lower() == "lazy"]
    if p.imgs and len(lazy) == len(p.imgs) and len(p.imgs) > 1:
        W("Todas as imagens com loading=lazy; a principal (LCP) não deve ter lazy")
    if p.imgs and not lazy and len(p.imgs) > 3:
        W("Nenhuma imagem com loading=lazy")

    # --- Scripts / performance
    head_scripts_blocking = [
        s for s in p.scripts
        if s.get("src") and not any(k in s for k in ("async", "defer"))
        and (s.get("type") or "") != "module"
    ]
    if head_scripts_blocking:
        W(f"{len(head_scripts_blocking)} <script src> sem async/defer (bloqueia renderização)")
    if re.search(r"jquery", html, re.I):
        W("jQuery detectado; avalie se é realmente necessário")
    if re.search(r"http://(?!localhost|127\.0\.0\.1|www\.w3\.org|schema\.org)", html):
        W("Referência http:// encontrada (conteúdo misto/sem HTTPS)")
    if re.search(r"lorem ipsum|\bTODO\b|\[PREENCHER", html, re.I):
        W("Há placeholders/lorem ipsum/TODO/[PREENCHER] — resolver ou informar ao usuário")
    if len(html.encode("utf-8")) > 200_000:
        W("HTML com mais de 200 KB; considere reduzir")

    # --- Acessibilidade / links
    for f in p.fields:
        fid = f.get("id")
        if not (fid in p.labels_for or f.get("aria-label") or f.get("aria-labelledby")):
            W(f"Campo sem label associado: {f.get('name') or f.get('id') or f.get('type')}")
    for a in p.anchors:
        txt = a["text"].strip().lower()
        if txt in ("clique aqui", "saiba mais", "aqui", "veja mais") and not a["attrs"].get("aria-label"):
            W(f"Link com texto genérico: \"{txt}\"")
        if a["attrs"].get("target") == "_blank" and "noopener" not in (a["attrs"].get("rel") or ""):
            W(f"target=_blank sem rel=noopener: {a['attrs'].get('href')}")
    if not any("icon" in (l.get("rel") or "").lower() for l in p.links):
        W("Sem favicon (<link rel=\"icon\">)")

    # CSS: sinais de mobile-first
    if re.search(r"<style|\.css", html, re.I) and not re.search(r"@media|min-width|clamp\(|flex|grid", html, re.I):
        W("Nenhum sinal de layout responsivo (@media/flex/grid) encontrado")

    return errors, warns


def collect(targets):
    files = []
    for t in targets:
        p = Path(t)
        if p.is_dir():
            files += sorted(p.rglob("*.html"))
        elif p.is_file():
            files.append(p)
        else:
            print(f"Não encontrado: {t}", file=sys.stderr)
    return files


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    files = collect(sys.argv[1:])
    if not files:
        print("Nenhum arquivo .html encontrado.")
        sys.exit(2)
    total_err = 0
    for f in files:
        errs, warns = audit(f)
        total_err += len(errs)
        status = "OK" if not errs else "FALHOU"
        print(f"\n=== {f} — {status} ({len(errs)} erros, {len(warns)} avisos)")
        for e in errs:
            print(f"  [ERRO]  {e}")
        for w in warns:
            print(f"  [AVISO] {w}")
    # arquivos de raiz recomendados
    roots = {f.parent for f in files}
    for r in roots:
        for name in ("robots.txt", "sitemap.xml"):
            if not (r / name).exists():
                print(f"\n[AVISO] {r}/{name} não encontrado (necessário na raiz do site)")
    print()
    sys.exit(1 if total_err else 0)


if __name__ == "__main__":
    main()
