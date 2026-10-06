#!/usr/bin/env python3
"""
Crea in Stripe un Payment Link per ogni prodotto del negozio che non ne ha ancora uno,
e salva i link in ../stripe-links.json (che il sito legge in automatico).

Perché: il sito vende tramite Payment Link Stripe, uno per prodotto. Farli a mano per decine
di prodotti è lungo. Questo script li crea tutti, già con:
  - prezzo e foto del prodotto
  - raccolta dell'indirizzo di spedizione (paesi in SHIP_TO) e del telefono
  - limite di 1 vendita per i pezzi unici: dopo il primo acquisto il link si disattiva da solo
  - ritorno al sito su ?ordine=ok (banner "Ordine completato!")

Uso (PowerShell, dalla cartella del progetto):

    $env:STRIPE_SECRET_KEY = "sk_test_..."        # prima prova con la chiave di TEST
    python tools/create-stripe-links.py            # anteprima: non crea nulla
    python tools/create-stripe-links.py --apply    # crea davvero i link

Per vendere sul serio ripeti con la chiave LIVE (sk_live_... oppure una chiave "ristretta" con
permessi di scrittura su Products, Prices e Payment Links) e cancella prima stripe-links.json
se contiene link di test. La chiave resta solo nella tua sessione: non va mai scritta nei file.

Opzionale: STRIPE_SHIPPING_RATE_ID = id di una tariffa di spedizione creata in Stripe
(Dashboard > Prodotti > Tariffe di spedizione), da aggiungere ai link.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

SITE_URL = os.environ.get("SITE_URL", "https://boutiquelm.web.app")
FIRESTORE = ("https://firestore.googleapis.com/v1/projects/boutiquelm/databases/(default)/documents"
             "/artifacts/boutique-lm-app/public/data/products?pageSize=300")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "stripe-links.json")
# Paesi verso cui si spedisce (codici ISO). Modificare qui se cambia la politica di spedizione.
SHIP_TO = ["IT", "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IE", "LV", "LT",
           "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE", "CH", "GB", "MC", "SM", "VA", "NO", "US"]


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


def load_products():
    d = json.load(urllib.request.urlopen(FIRESTORE))
    out = []
    for doc in d.get("documents", []):
        f = {k: val(v) for k, v in doc["fields"].items()}
        f["id"] = doc["name"].split("/")[-1]
        out.append(f)
    return out


def stripe(path, data, key):
    """POST form-encoded a Stripe; i campi annidati usano la notazione a[b][c]."""
    pairs = []

    def flat(prefix, v):
        if isinstance(v, dict):
            for k, x in v.items():
                flat(f"{prefix}[{k}]", x)
        elif isinstance(v, list):
            for i, x in enumerate(v):
                flat(f"{prefix}[{i}]", x)
        else:
            pairs.append((prefix, str(v)))

    for k, v in data.items():
        flat(k, v)
    req = urllib.request.Request("https://api.stripe.com/v1/" + path, data=urllib.parse.urlencode(pairs).encode(),
                                 headers={"Authorization": "Bearer " + key})
    try:
        return json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e:
        sys.exit(f"Errore Stripe ({e.code}) su {path}: {e.read().decode()[:400]}")


def main():
    apply = "--apply" in sys.argv
    key = os.environ.get("STRIPE_SECRET_KEY", "")
    if apply and not key.startswith(("sk_", "rk_")):
        sys.exit("Imposta prima la chiave: $env:STRIPE_SECRET_KEY = \"sk_test_...\"")
    shipping_rate = os.environ.get("STRIPE_SHIPPING_RATE_ID", "")

    try:
        links = json.load(open(OUT, encoding="utf-8"))
    except (OSError, ValueError):
        links = {}

    todo = []
    for p in load_products():
        if p.get("isService") or p.get("price", 0) <= 0:
            continue
        if links.get(p["id"]) or "buy.stripe.com" in (p.get("stripeUrl") or ""):
            continue
        stock = p.get("stock", 0) if not p.get("variants") else sum((p.get("variantsStock") or {}).values())
        if stock <= 0:
            continue
        todo.append((p, stock))

    print(f"{len(todo)} prodotti senza link di pagamento.")
    for p, stock in todo:
        print(f"  - {p['name'].strip()[:60]:60} EUR {p['price']:>7}  pezzi: {stock}")
    if not apply:
        print("\nAnteprima: non è stato creato nulla. Aggiungi --apply per creare i link.")
        return

    for p, stock in todo:
        image = (p.get("images") or [p.get("image")] or [""])[0]
        product = stripe("products", {"name": p["name"].strip()[:250], "images": [image] if image else [],
                                      "metadata": {"firestore_id": p["id"]}}, key)
        price = stripe("prices", {"product": product["id"], "currency": "eur",
                                  "unit_amount": int(round(p["price"] * 100))}, key)
        link = {
            "line_items": [{"price": price["id"], "quantity": 1}],
            "after_completion": {"type": "redirect", "redirect": {"url": SITE_URL + "/?ordine=ok"}},
            "shipping_address_collection": {"allowed_countries": SHIP_TO},
            "phone_number_collection": {"enabled": "true"},
            # Pezzo unico (o stock limitato): il link si chiude dopo questo numero di vendite
            "restrictions": {"completed_sessions": {"limit": stock}},
        }
        if shipping_rate:
            link["shipping_options"] = [{"shipping_rate": shipping_rate}]
        pl = stripe("payment_links", link, key)
        links[p["id"]] = pl["url"]
        with open(OUT, "w", encoding="utf-8") as f:   # salva dopo ogni link: si può riprendere se si interrompe
            json.dump(links, f, indent=1)
        print("  creato:", p["name"].strip()[:50], "->", pl["url"])
    print(f"\nFatto. {len(links)} link in stripe-links.json. Ora pubblica il sito (firebase deploy --only hosting).")


if __name__ == "__main__":
    main()
