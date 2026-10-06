#!/usr/bin/env python3
"""
Genera le pagine che Google può indicizzare: una pagina statica per ogni prodotto (italiano e inglese),
sitemap.xml e robots.txt.

Perché: il negozio è una "single page app": i prodotti compaiono solo dopo che JavaScript li ha
caricati dal database, e Google li vede male o non li vede. Queste pagine contengono già testo, foto,
prezzo e dati strutturati (schema.org/Product) e rimandano al negozio con un pulsante.

Quando lanciarlo: ogni volta che aggiungi, togli o modifichi prodotti (o cambi dominio), poi pubblica:

    python tools/build-seo.py
    npx firebase deploy --only hosting

Dominio: di default usa https://boutiquelm.web.app. Quando boutiquelm.it sarà attivo:

    $env:SITE_URL = "https://boutiquelm.it"; python tools/build-seo.py

Non richiede chiavi né login: legge il catalogo pubblico da Firestore.
"""
import html
import json
import os
import re
import shutil
import unicodedata
import urllib.request
from datetime import date

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SITE = os.environ.get("SITE_URL", "https://boutiquelm.web.app").rstrip("/")
FIRESTORE = ("https://firestore.googleapis.com/v1/projects/boutiquelm/databases/(default)/documents"
             "/artifacts/boutique-lm-app/public/data/products?pageSize=300")
BRAND = "Boutique LM"

TXT = {
    "it": {"cta": "Vai al negozio", "home": "Boutique LM — Luxury Reselling & Atelier Services",
           "soldout": "Esaurito", "avail": "Disponibile", "brand": "Brand", "cond": "Condizione", "mat": "Materiale",
           "tagline": "Borse e accessori di lusso autentici, selezionati e autenticati. Firenze.",
           "suffix": "Boutique LM — Luxury Reselling Firenze"},
    "en": {"cta": "View in the shop", "home": "Boutique LM — Luxury Reselling & Atelier Services",
           "soldout": "Sold out", "avail": "Available", "brand": "Brand", "cond": "Condition", "mat": "Material",
           "tagline": "Authentic luxury bags and accessories, selected and authenticated. Florence, Italy.",
           "suffix": "Boutique LM — Luxury Reselling Florence"},
}


# Valori ricorrenti tradotti nelle pagine inglesi (gli altri restano com'è)
VALUES_EN = {
    "Borse & Pouch": "Bags & Pouches", "Piccola Pelletteria": "Small Leather Goods", "Valigie": "Luggage",
    "Nuovo": "New", "Usato": "Used", "Come Nuova": "Like New", "Pari al Nuovo": "As Good as New",
    "Usato, pari al nuovo": "Used, as good as new", "Pelle": "Leather", "Pelle di Pitone": "Python Leather",
    "Pelle Verniciata": "Patent Leather", "Pelle, tessuto": "Leather, fabric", "Nylon, Pelle": "Nylon, Leather",
}


def tr(v, lang):
    v = (v or "").strip()
    return VALUES_EN.get(v, v) if lang == "en" else v


def val(x):
    k = next(iter(x))
    v = x[k]
    if k == "integerValue":
        return int(v)
    if k == "doubleValue":
        return float(v)
    if k == "arrayValue":
        return [val(i) for i in v.get("values", [])]
    if k == "mapValue":
        return {a: val(b) for a, b in v.get("fields", {}).items()}
    return v


def slugify(name, pid):
    # Deve restare identica a slugifyProduct() in index.html
    s = unicodedata.normalize("NFD", (name or "").lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60].strip("-")
    return (s + "-" if s else "") + pid[:6].lower()


def summary(desc, n=155):
    t = re.sub(r"[•\*]+", " ", desc or "")
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) <= n:
        return t
    return t[:n].rsplit(" ", 1)[0].rstrip(",.;:- ") + "…"


def esc(s):
    return html.escape(s or "", quote=True)


def total_stock(p):
    if p.get("variants"):
        return sum((p.get("variantsStock") or {}).values())
    return p.get("stock", 0) or 0


def main():
    d = json.load(urllib.request.urlopen(FIRESTORE))
    try:
        en_file = json.load(open(os.path.join(ROOT, "products-en.json"), encoding="utf-8"))
    except (OSError, ValueError):
        en_file = {}

    products = []
    for doc in d.get("documents", []):
        f = {k: val(v) for k, v in doc["fields"].items()}
        f["id"] = doc["name"].split("/")[-1]
        if f.get("isService") or (f.get("price") or 0) <= 0:
            continue
        products.append(f)

    out_dir = os.path.join(ROOT, "p")
    shutil.rmtree(out_dir, ignore_errors=True)
    os.makedirs(os.path.join(out_dir, "en"))

    sitemap = []
    for p in products:
        slug = slugify(p.get("name"), p["id"])
        en = en_file.get(p["id"], {})
        has_en = bool(p.get("description_en") or en.get("description_en") or not (p.get("description") or "").strip())
        langs = ["it"] + (["en"] if has_en else [])
        url = {l: f"{SITE}/p/{'en/' if l == 'en' else ''}{slug}.html" for l in langs}
        images = [i for i in (p.get("images") or [p.get("image")]) if i]
        for lang in langs:
            t = TXT[lang]
            name = (p.get("name_en") or en.get("name_en") or p["name"]) if lang == "en" else p["name"]
            desc = ((p.get("description_en") or en.get("description_en") or "") if lang == "en" else p.get("description") or "")
            name = name.strip()
            in_stock = total_stock(p) > 0
            cond = (p.get("condition") or "").strip()
            ld = {
                "@context": "https://schema.org", "@type": "Product", "name": name, "image": images[:6],
                "description": summary(desc, 500) or name, "sku": p.get("internalCode") or p["id"],
                "brand": {"@type": "Brand", "name": (p.get("brand") or BRAND).strip() or BRAND},
                "offers": {"@type": "Offer", "url": url[lang], "priceCurrency": "EUR", "price": f"{p['price']:.2f}",
                           "availability": "https://schema.org/InStock" if in_stock else "https://schema.org/SoldOut",
                           "itemCondition": "https://schema.org/NewCondition" if cond.lower().startswith("nuovo") else "https://schema.org/UsedCondition",
                           "seller": {"@type": "Organization", "name": BRAND}},
            }
            alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{esc(url[l])}">' for l in langs)
            alts += f'<link rel="alternate" hreflang="x-default" href="{esc(url["it"])}">' if len(langs) > 1 else ""
            body_desc = "".join(f"<p>{esc(x)}</p>" for x in desc.strip().split("\n") if x.strip())
            facts = "".join(f"<li><b>{lab}:</b> {esc(v)}</li>" for lab, v in
                            ((t["brand"], p.get("brand")), (t["cond"], tr(p.get("condition"), lang)), (t["mat"], tr(p.get("material"), lang))) if v)
            shop = f"{SITE}/?id={p['id']}&lang={lang}"
            page = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(name)} | {t['suffix']}</title>
<meta name="description" content="{esc(summary(desc) or name)}">
<link rel="canonical" href="{esc(url[lang])}">
{alts}
<meta property="og:type" content="product">
<meta property="og:title" content="{esc(name)} | {BRAND}">
<meta property="og:description" content="{esc(summary(desc) or name)}">
<meta property="og:url" content="{esc(url[lang])}">
{f'<meta property="og:image" content="{esc(images[0])}">' if images else ''}
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>
body{{margin:0;font-family:Georgia,'Times New Roman',serif;background:#fafafa;color:#18181b}}
main{{max-width:960px;margin:0 auto;padding:32px 20px}}
a{{color:inherit}} .brand{{letter-spacing:.2em;text-transform:uppercase;font:700 12px/1 system-ui,sans-serif;text-decoration:none}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:40px;margin-top:28px}} img{{width:100%;height:auto;aspect-ratio:1;object-fit:cover}}
h1{{font-size:34px;line-height:1.15;margin:0 0 12px}} .price{{font:300 26px system-ui,sans-serif;margin:0 0 20px}}
.desc{{font:16px/1.6 system-ui,sans-serif;color:#52525b}} ul{{font:14px/1.8 system-ui,sans-serif;padding-left:18px}}
.cta{{display:inline-block;background:#000;color:#fff;padding:16px 28px;font:700 11px system-ui,sans-serif;letter-spacing:.2em;text-transform:uppercase;text-decoration:none;margin-top:16px}}
.tag{{font:700 11px system-ui,sans-serif;letter-spacing:.15em;text-transform:uppercase;color:#a1a1aa}}
@media(max-width:700px){{.grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<main>
<a class="brand" href="{SITE}/?lang={lang}">{BRAND}</a>
<div class="grid">
<div>{f'<img src="{esc(images[0])}" alt="{esc(name)}">' if images else ''}</div>
<div>
<p class="tag">{esc(tr(p.get('category'), lang))}</p>
<h1>{esc(name)}</h1>
<p class="price">€{p['price']:.2f} — {t['avail'] if in_stock else t['soldout']}</p>
<ul>{facts}</ul>
<div class="desc">{body_desc}</div>
<a class="cta" href="{esc(shop)}">{t['cta']}</a>
</div>
</div>
<p class="desc" style="margin-top:40px">{t['tagline']}</p>
</main>
</body>
</html>
"""
            path = os.path.join(out_dir, "en" if lang == "en" else "", slug + ".html")
            open(path, "w", encoding="utf-8", newline="\n").write(page)
        alt_xml = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{esc(url[l])}"/>' for l in langs)
        for l in langs:
            sitemap.append(f"<url><loc>{esc(url[l])}</loc>{alt_xml if len(langs) > 1 else ''}<changefreq>weekly</changefreq></url>")

    today = date.today().isoformat()
    static = [f"{SITE}/", f"{SITE}/legal/terms.html", f"{SITE}/legal/privacy.html", f"{SITE}/legal/cookies.html"]
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
           + "\n".join(f"<url><loc>{u}</loc><lastmod>{today}</lastmod></url>" for u in static) + "\n"
           + "\n".join(sitemap) + "\n</urlset>\n")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n").write(xml)
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8", newline="\n").write(
        f"User-agent: *\nAllow: /\nDisallow: /tools/\n\nSitemap: {SITE}/sitemap.xml\n")
    n_pages = sum(len(os.listdir(os.path.join(out_dir, x))) - (1 if x == "" else 0) for x in ("", "en"))
    print(f"{len(products)} prodotti -> {n_pages} pagine in /p, sitemap.xml ({len(sitemap) + len(static)} indirizzi) e robots.txt. Dominio: {SITE}")


if __name__ == "__main__":
    main()
