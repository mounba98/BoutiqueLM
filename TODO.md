# ✅ Boutique LM — Cose da fare (solo te, niente codice)

Tutto il codice è completo e in produzione su https://boutiquelm.it
Le azioni qui sotto sono solo configurazione e gestione operativa.

---

## 🔴 Prima del lancio marketing (urgente)

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

*Ultimo aggiornamento codice: 20 Giugno 2026*
*Sito live: https://boutiquelm.it | https://boutiquelm.web.app*
