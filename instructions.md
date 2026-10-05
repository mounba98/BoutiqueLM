# GUIDA GESTIONE SITO - BOUTIQUE LM (ATELIER)

Benvenuto nella guida di gestione per Boutique LM. Grazie al nuovo pannello di amministrazione, non è più necessario modificare il codice sorgente del sito per gestire i pagamenti, i prodotti o l'Intelligenza Artificiale. Tutto si gestisce direttamente dall'interfaccia web.

---

## 1. CONFIGURAZIONE DEI PAGAMENTI (STRIPE)

Il sito utilizza i **Link di Pagamento Stripe** (Stripe Payment Links). Per configurare i pagamenti reali con carta di credito:

1. **Crea un Account Stripe**: Vai su [stripe.com](https://stripe.com) e registra il tuo account aziendale.
2. **Crea un Prodotto su Stripe**:
   - Nella dashboard di Stripe, vai su **Prodotti** > **Aggiungi Prodotto**.
   - Inserisci il nome dell'articolo (es. *Borsa Pouch Upcycled*), carica una foto e imposta il prezzo.
   - Salva il prodotto.
3. **Genera il Link di Pagamento**:
   - Accanto al prodotto creato su Stripe, clicca su **Crea Link di Pagamento** (Payment Link).
   - Personalizza la pagina di pagamento se desideri (es. richiedendo l'indirizzo di spedizione, che è fondamentale per spedire la merce!).
   - Clicca su **Crea Link** in alto a destra e **copia il link** generato (avrà un formato tipo `https://buy.stripe.com/abc123xyz...`).
4. **Collega il Link al Prodotto sul Sito**:
   - Accedi all'area riservata del tuo sito inserendo `#admin` in fondo all'indirizzo (es. `https://tuosito.it/#admin`).
   - Loggati con le tue credenziali Admin.
   - Nella scheda **Inventario**, trova il prodotto che vuoi collegare e clicca sull'icona **Modifica 📝** (matita).
   - Nel campo **Link Stripe**, incolla il link copiato in precedenza.
   - Clicca su **Salva nel Database** in fondo alla pagina.

*Nota: I servizi (es. Restauro o preventivi con prezzo negativo) non utilizzano i link Stripe, poiché reindirizzano automaticamente i clienti a scrivervi su WhatsApp o E-mail.*

---

## 2. GESTIONE PRODOTTI & INVENTARIO

Puoi aggiungere, modificare o eliminare prodotti in qualsiasi momento dall'area riservata:

* **Aggiungere un Prodotto**:
  - Vai sulla scheda **Nuovo Prodotto**.
  - Compila i campi obbligatori (Nome, Categoria, Prezzo). Il campo **Codice Interno** può essere generato automaticamente cliccando su **Genera 🔄** (creerà un codice univoco stile `BLM-BOR-GU-001` che incrementa da solo in base alla categoria e al marchio e che previene i duplicati).
  - Se usi il telefono, puoi cliccare su **Carica Immagine ⬆️** per selezionare una foto dalla galleria o **attivare direttamente la fotocamera del telefono** per scattare una foto al momento.
  - Per riordinare o eliminare le immagini caricate, usa il tasto **"X"** rosso sopra la miniatura.
  - Clicca su **Salva nel Database**.
* **Gestione Categorie**:
  - Se desideri aggiungere o modificare le categorie, puoi selezionare "Aggiungi Categoria" nel form, oppure usare lo strumento **Gestione Categorie** nella sezione *Configurazione Globale* per rinominare o unire categorie esistenti.
* **Esportare l'Inventario**:
  - Nella scheda **Inventario**, clicca sul pulsante verde **Esporta CSV 📥** per scaricare un file Excel contenente tutto l'elenco dei prodotti, stock, prezzi e codici.

---

## 3. CONFIGURAZIONE AI (GEMINI)

Il sito utilizza l'Intelligenza Artificiale di Google Gemini per lo *Stylist Personale* e per evocare le *Storie del Vintage*:

1. Ottieni una chiave API gratuita andando su [Google AI Studio](https://aistudio.google.com/).
2. Accedi al pannello `#admin` del tuo sito.
3. Nella scheda **Nuovo Prodotto**, individua la sezione **⚙️ Configurazione Globale** in alto.
4. Incolla la tua chiave nel campo **Gemini API Key** e clicca su **Salva Key**.
5. Da questo momento, l'AI è attiva e i clienti potranno usarla direttamente sul sito!
