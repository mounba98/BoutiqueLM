# Boutique LM

Sito e-commerce di **Boutique LM — Luxury Reselling & Atelier Services**: vendita di
articoli di lusso di seconda mano e servizi di atelier.

- Sito live: https://boutiquelm.it (alias: https://boutiquelm.web.app)
- Progetto Firebase: `boutiquelm`

## Stack

| Parte | Tecnologia |
|---|---|
| Frontend | Un unico `index.html` (HTML + JavaScript, nessun framework né build) |
| Stile e icone | Tailwind CSS (CDN) e Lucide (unpkg) |
| Database e immagini | Firebase Firestore e Firebase Storage |
| Accesso admin | Firebase Authentication (email/password) |
| Hosting | Firebase Hosting |
| Pagamenti | Stripe Payment Links (uno per prodotto) |
| AI (stylist e storie vintage) | Google Gemini, con chiave salvata dal pannello admin |
| Statistiche | Google Analytics |

## Funzionalità

- Catalogo dinamico da Firestore, filtri per categoria, ordinamento, sezione "In Vetrina".
- Dettaglio prodotto con galleria, varianti (taglia/colore) e stock per variante.
- Carrello e pagamento tramite link Stripe; i servizi (restauro, preventivi) rimandano a WhatsApp o e-mail.
- Pannello admin su `/#admin`: prodotti, stock, categorie, priorità vetrina, esportazione CSV, configurazione AI.

## Struttura della cartella

```
index.html          Il sito (frontend + pannello admin)
legal/              Privacy, cookie, termini
logo.png            Logo
firebase.json       Configurazione Hosting, Firestore e Storage
.firebaserc         Progetto Firebase collegato
firestore.rules     Regole di sicurezza del database
storage.rules       Regole di sicurezza delle immagini
start_server.cmd    Avvio in locale (Windows)
deploy_website.cmd  Pubblicazione guidata (Windows)
overview.md         Panoramica del progetto e istruzioni d'uso
instructions.md     Guida alla gestione di Stripe, prodotti e AI
TODO.md             Cose da fare e operatività quotidiana
index backup.html   Vecchia copia di sicurezza, non più usata
```

## Come avviarlo in locale

Serve Node.js. Poi, dalla cartella del progetto:

```bash
npx serve .
```

oppure doppio clic su `start_server.cmd`. Apri l'indirizzo che compare nel terminale.

**Attenzione:** anche in locale il sito usa il database Firebase di produzione. Quello che
modifichi dal pannello admin cambia i dati reali del negozio.

## Come pubblicarlo

```bash
npx firebase login
npx firebase deploy
```

oppure `deploy_website.cmd`, che guida i passaggi. Il deploy pubblica anche le regole di
sicurezza di Firestore e Storage definite in questa cartella.

## Sicurezza

- Le regole in `firestore.rules` e `storage.rules` permettono la **lettura pubblica** dei
  prodotti e la **scrittura solo a utenti autenticati** (l'admin). Tutto il resto è bloccato.
- Dopo ogni modifica alle regole, controlla nella Console Firebase che quelle attive siano
  le stesse dei file.
- La chiave Firebase presente in `index.html` è una chiave web pubblica per progettazione:
  la protezione sono le regole sopra, non la chiave.
- La chiave Gemini **non** è nel codice: si imposta dal pannello admin e resta in Firestore,
  leggibile solo da utenti autenticati.
- Non salvare nel repository password, chiavi API private o file `.env`.

## Gestione quotidiana

- Gli ordini arrivano solo su https://dashboard.stripe.com (e per e-mail da Stripe), non nel pannello admin.
- Quando vendi un pezzo, azzera lo stock da `/#admin` → Inventario → Modifica.
- Istruzioni complete: `overview.md`, `instructions.md`, `TODO.md`.
