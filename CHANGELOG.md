# Boutique LM — Registro delle modifiche

Qui si annota ogni modifica al sito: cosa è cambiato, perché, e se è stato pubblicato.
Le più recenti sono in alto. Ogni voce corrisponde a uno o più commit su GitHub.

## Da fare (in ordine di priorità)

1. Pagamento: carrello con più articoli (Stripe accetta un prodotto per volta).
2. Stock: il sito non riesce a scalare lo stock (le regole del database lo impediscono ai visitatori).
3. AI Stylist: risulta sempre offline per i visitatori.
4. Parte legale: banner cookie con consenso, pagine legali in inglese, spedizioni internazionali.
5. Indicizzazione Google (SEO): sitemap, robots, pagine prodotto indicizzabili, dati strutturati.
6. Dominio `boutiquelm.it`: da acquistare e collegare a Firebase Hosting (azione manuale del proprietario).

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
