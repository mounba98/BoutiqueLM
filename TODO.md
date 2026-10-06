# ✅ Boutique LM — Cose da fare (solo te, niente codice)

Il sito è online su https://boutiquelm.web.app (il dominio boutiquelm.it non è ancora attivo).
Lo storico delle modifiche è in `CHANGELOG.md`.

---

## 🔴 Per poter vendere online (urgente)

### 1. Crea i link di pagamento Stripe (automatico)
Finché un prodotto non ha il link Stripe, "Procedi al pagamento" apre WhatsApp / e-mail con l'ordine già scritto.
Per creare tutti i link in un colpo (con indirizzo di spedizione, telefono e limite di 1 vendita per i pezzi unici):
1. Su https://dashboard.stripe.com crea una **chiave API** (Sviluppatori → Chiavi API). Prima prova con la chiave di **test** (`sk_test_…`).
2. (Facoltativo) Crea una tariffa di spedizione in Stripe (Prodotti → Tariffe di spedizione) e copia il suo id (`shr_…`).
3. Apri PowerShell nella cartella del progetto e lancia:
```
$env:STRIPE_SECRET_KEY = "sk_test_..."
$env:STRIPE_SHIPPING_RATE_ID = "shr_..."        # solo se l'hai creata
python tools/create-stripe-links.py              # anteprima, non crea nulla
python tools/create-stripe-links.py --apply      # crea i link
npx firebase deploy --only hosting               # li pubblica
```
4. Prova un acquisto di test (carta `4242 4242 4242 4242`). Poi ripeti con la chiave **live**, dopo aver svuotato `stripe-links.json` (`{}`).
5. Mai scrivere la chiave in un file o inviarla in chat: va solo nella sessione di PowerShell.

Per un prodotto nuovo basta rilanciare lo script: crea solo i link mancanti. Un link impostato a mano nel campo "Link Stripe" dell'admin ha la precedenza.

### 2. AI Stylist: limita la chiave e pubblica le regole
L'AI Stylist non rispondeva perché Google ha ritirato il modello e la chiave non era leggibile dai visitatori.
Il codice è già corretto; mancano due azioni tue:
1. https://console.cloud.google.com → API e servizi → Credenziali → apri la chiave Gemini → **Restrizioni applicazione: Referrer HTTP**
   (`boutiquelm.web.app/*` e `boutiquelm.it/*`) → **Restrizioni API: solo Generative Language API** → imposta una quota giornaliera bassa.
2. Poi pubblica le regole: `npx firebase deploy --only firestore:rules`
   (rende leggibile a tutti `config/settings`, che contiene solo la chiave).

### 3. Compila i dati legali
Nei file `legal/terms.html` e `legal/privacy.html` cerca le scritte su sfondo giallo: ragione sociale, P.IVA, sede, regime IVA.
Fai rivedere le pagine da un commercialista o da un legale prima di vendere all'estero.

### 4. Dominio boutiquelm.it
1. Acquista il dominio.
2. Console Firebase → Hosting → **Aggiungi dominio personalizzato** e segui i passaggi DNS.
3. Rigenera la SEO con il nuovo dominio:
```
$env:SITE_URL = "https://boutiquelm.it"; python tools/build-seo.py
```
   e sostituisci `https://boutiquelm.web.app` con `https://boutiquelm.it` in `index.html` (canonical, hreflang, dati strutturati)
   e nel link di ritorno dei Payment Link Stripe (`/?ordine=ok`). Poi `npx firebase deploy --only hosting`.

---

## 🟡 Per avere più traffico (SEO)

- Dopo ogni modifica al catalogo: `python tools/build-seo.py` e `npx firebase deploy --only hosting`
  (aggiorna le pagine prodotto indicizzabili, `sitemap.xml` e `robots.txt`).
- Registra il sito su https://search.google.com/search-console e invia `sitemap.xml`.
- Compila "Description (EN)" per i prodotti nuovi (o usa "✨ Traduci in inglese" nell'admin): le pagine inglesi servono per essere trovati dall'estero.
- Metti nel profilo Instagram e TikTok il link al sito e usa i link `…/p/<prodotto>.html` nei post.

---

## 🔧 Dati prodotto da correggere (admin)

- "Fendi Valigia Vintage Zucca FF" ha la descrizione di una Prada Business Bag.
- Senza descrizione: Fendi Baguette, Maison Margiela Bag on Chain, Gucci Microguccissima, Prada Saffiano, Burberry Card Case (Pelle Cuoio), Keyholder.
- Due "Cardholder Moschino Couture" hanno lo stesso nome e colori diversi: meglio distinguerli nel nome.

---

## 🔴 Prima del lancio marketing

### 1. Elimina i prodotti di test
- Vai su boutiquelm.it/#admin → login → tab **Inventario**
- Elimina tutti i prodotti con immagini placeholder o nomi di test (es. "Prova 3")

### 2. Carica i prodotti reali con foto vere
- Admin → **Nuovo Prodotto**
- Carica foto reali con il pulsante "📸 Carica Foto"
- Compila tutti i campi: nome, brand, prezzo, condizione, materiale, seriale, stock

### 3. Per prodotti di abbigliamento: usa le Varianti per le taglie
- Admin → Nuovo Prodotto → sezione **Varianti**
- Nel campo "Etichetta variante" scrivi: `Taglia`
- Aggiungi ogni taglia come variante: `XS`, `S`, `M`, `L`, `XL`
  oppure numeriche: `38`, `40`, `42`, `44`
- Ogni variante ha il suo stock separato
- Il numero di pezzi disponibili NON viene mostrato al cliente (vede solo "Disponibile"/"Esaurito")

### 4. Imposta la Vetrina
- Per ogni prodotto che vuoi in "In Vetrina" (i più belli/importanti):
- Admin → modifica prodotto → campo **"Priorità Vetrina"** → inserisci un numero da 1 a 10
- I 4 prodotti con priorità più alta appaiono nella sezione "In Vetrina" in home

### 5. Imposta le foto copertina delle categorie (consigliato)
- Admin → tab **Categorie**
- Clicca sulla miniatura di ogni categoria per caricare una foto copertina
- Imposta l'ordine in cui appaiono le sezioni nella home
- Clicca **💾 Salva Configurazione**

### 6. Aggiorna le regole di sicurezza Firebase
- Leggi le istruzioni nella sezione 🔒 del file `overview.md` in questa cartella
- Vai su https://console.firebase.google.com → progetto `boutiquelm`
- **Firestore → Regole**: applica le regole dal file `firestore.rules`
- **Storage → Regole**: applica le regole dal file `storage.rules`
- ⚠️ Senza questo, chiunque potrebbe scrivere nel database

---

## 🟡 Dopo il lancio (non urgente)

### 7. Collega Stripe al banner di ringraziamento
- Per ogni Payment Link su dashboard.stripe.com:
- Apri il link → **After payment** → **Redirect to URL**
- Inserisci: `https://boutiquelm.it?ordine=ok`
- Dopo ogni acquisto il cliente vedrà il banner "Ordine completato!"

### 8. Imposta i link Stripe sui prodotti
- Per ogni prodotto che ha un prezzo > 0:
- Admin → modifica prodotto → campo **"Link Stripe (Payment Link)"**
- Incolla il link del Payment Link Stripe corrispondente

### 9. Imposta i limiti di quantità su Stripe (anti-doppio acquisto)
- Per ogni Payment Link su dashboard.stripe.com:
- Apri il link → modifica → cerca **"Quantity"** o **"Inventory"**
- Imposta la quantità massima uguale al tuo stock (es. 1 per pezzi unici)
- Stripe blocca automaticamente il secondo acquisto se il primo è già completato
- ⚠️ Senza questo, due persone potrebbero comprare lo stesso pezzo unico

### 10. Verifica Google Analytics
- Vai su https://analytics.google.com
- Il tuo ID è già nel codice: `G-EENPRN5PVL`
- Controlla che stia ricevendo dati (sezione "Tempo reale")

---

## 🔵 Operatività quotidiana — IMPORTANTE

### Dove arrivano gli ordini
- Gli ordini arrivano SOLO su **https://dashboard.stripe.com**
- Ricevi anche una **email da Stripe** per ogni pagamento completato
- L'admin panel di Boutique LM non riceve ordini — serve solo per il catalogo

### Cosa fare quando vendi un pezzo
```
1. Stripe ti invia email di pagamento completato
2. Vai su boutiquelm.it/#admin → login
3. Tab Inventario → trova il prodotto venduto → ✏️ Modifica
4. Se pezzo unico: cambia stock a 0
5. Se vestiario con taglie: riduci lo stock della taglia venduta a 0
6. Salva → il sito mostra "Esaurito" automaticamente in tempo reale
```

Questo richiede circa 30-60 secondi dopo la notifica di pagamento.

### Se vuoi che lo stock si aggiorni automaticamente
Richiederebbe un backend con Firebase Functions (piano Blaze ~10€/mese) e
un webhook Stripe collegato al database. Da valutare solo se il volume di
vendite cresce significativamente e la gestione manuale diventa onerosa.

---

*Ultimo aggiornamento: 6 Ottobre 2026*
*Sito live: https://boutiquelm.web.app*
