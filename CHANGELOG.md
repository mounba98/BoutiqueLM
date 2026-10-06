# Boutique LM — Registro delle modifiche

Qui si annota ogni modifica al sito: cosa è cambiato, perché, e se è stato pubblicato.
Le più recenti sono in alto. Ogni voce corrisponde a uno o più commit su GitHub.

## Da fare (in ordine di priorità)

Azioni del proprietario (non si possono fare da codice):
1. **Stripe**: creare i link di pagamento con `tools/create-stripe-links.py` (vedi TODO.md, punto 1). Finché mancano, "Procedi al pagamento" apre la scelta WhatsApp / e-mail.
2. **AI Stylist**: limitare la chiave Gemini nella Google Cloud Console e dare l'ok a pubblicare le regole Firestore già pronte (TODO.md, punto 2).
3. **Legale**: compilare i segnaposto gialli (ragione sociale, P.IVA, sede, regime IVA) in `legal/terms.html` e `legal/privacy.html`, poi farli rivedere da un professionista.
4. **Dominio** `boutiquelm.it`: acquistarlo e collegarlo a Firebase Hosting, poi rigenerare la SEO con `SITE_URL` (TODO.md, punto 4).
5. **Google Search Console**: inviare `sitemap.xml`.
6. Correggere nel database i dati dei prodotti (vedi TODO.md, sezione "Dati prodotto da correggere").

## 2026-10-06 — Pagamento, stock, AI, legale, SEO

**Pubblicato:** in corso (solo Hosting). Le regole Firestore NON sono state pubblicate.

Pagamento e stock
- Causa trovata: tutti i 33 prodotti hanno `stripeUrl` vuoto e nessuna variante; il checkout leggeva solo lo stock delle varianti e
  considerava ogni prodotto "esaurito". In più tentava di scalare lo stock dal browser, cosa che le regole Firestore vietano ai visitatori.
- `stockFor()` legge lo stock giusto (per variante o semplice). Rimosso lo scarico stock dal browser.
- Se per un articolo non c'è ancora il link Stripe, "Procedi al pagamento" apre la scelta WhatsApp / e-mail con l'ordine già scritto.
- Più articoli nel carrello: Stripe paga un prodotto per volta, quindi appare una finestra con un pulsante "Paga" per articolo.
  Il carrello ora si conserva nel browser e, al ritorno da Stripe (`?ordine=ok`), l'articolo pagato esce dal carrello.
- Nuovo `tools/create-stripe-links.py`: crea in Stripe prodotto, prezzo e Payment Link per ogni articolo, con raccolta
  indirizzo, telefono e limite di 1 vendita per i pezzi unici (il link si disattiva dopo l'acquisto). Salva `stripe-links.json`.
- Lo stock si azzera ancora a mano da `/#admin` dopo una vendita (TODO.md); l'automazione completa richiede Firebase Functions + webhook Stripe (piano Blaze).

AI Stylist
- Causa probabile dell'"offline": il modello `gemini-2.5-flash-preview-09-2025` risulta ritirato da Google, e la chiave
  è leggibile solo da utenti autenticati (quindi non dai visitatori).
- `callGemini()` ora prova `gemini-flash-latest`, poi `gemini-2.5-flash`, poi `gemini-2.0-flash`.
- `firestore.rules`: lettura pubblica di `config/settings` (contiene solo la chiave). **Da pubblicare solo dopo aver limitato la chiave** in Google Cloud.

Legale
- Banner cookie (Accetta / Rifiuta) e link "Preferenze cookie" nel footer; Google Analytics parte solo dopo il consenso.
- Pagine `legal/*` riscritte in italiano e inglese con selettore lingua: termini (spedizioni internazionali, recesso, garanzia, dazi),
  privacy (Stripe, Google/Gemini, trasferimenti extra-UE, diritti GDPR) e cookie. I segnaposto gialli vanno compilati dal titolare.
- Anno nel footer aggiornato al 2026.

SEO / indicizzazione
- `tools/build-seo.py`: genera una pagina statica per ogni prodotto in italiano e inglese (`/p/…`), con titolo, descrizione,
  Open Graph e dati strutturati schema.org/Product, più `sitemap.xml` e `robots.txt`. Da rilanciare quando cambia il catalogo.
- Home: canonical, hreflang IT/EN e dati strutturati `Store`. Le card prodotto sono ora link veri (il clic apre comunque la scheda).
- Dominio usato per ora: `https://boutiquelm.web.app` (`boutiquelm.it` non è ancora attivo).

## 2026-10-06 — Versione inglese del sito

**Pubblicato:** sì (solo Hosting).

- Nuovo sistema IT / EN: il sito parte in inglese se la lingua del browser non è l'italiano.
  Selettore IT / EN in alto (menu mobile incluso); la scelta viene ricordata; `?lang=en` o `?lang=it` forza la lingua.
- Tutta l'interfaccia (home, servizi, form, carrello, pagamento, avvisi, banner ordine) è tradotta
  tramite il dizionario `I18N_EN` in `index.html`. Per aggiungere una frase si aggiunge una riga al dizionario.
- Descrizioni, nomi e note brevi in inglese dei 33 prodotti esistenti: file `products-en.json`
  (chiave = id prodotto in Firestore). Non scrive nulla nel database.
- Pannello admin: nuovi campi "Name (EN)", "Description (EN)", "Short Note (EN)" e pulsante
  "✨ Traduci in inglese" (usa Gemini). I campi inglesi dell'admin hanno la precedenza su `products-en.json`.
- L'AI Stylist risponde in inglese quando il sito è in inglese.
- Restano in italiano: pagine `legal/*`, pannello admin, nomi delle varianti, testi liberi non presenti nel dizionario.

Dati da correggere nel database: la scheda "Fendi Valigia Vintage Zucca FF" ha la descrizione di una borsa Prada
Business Bag; cinque prodotti non hanno descrizione.
