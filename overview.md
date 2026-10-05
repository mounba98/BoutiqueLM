# Panoramica Progetto Boutique LM & Istruzioni Finali

## ✅ Stato del Progetto
Il progetto è giunto a uno stato di maturità funzionale completa. Ecco le funzionalità attive:

*   **Frontend E-Commerce**:
    *   Catalogo dinamico caricato da Firebase.
    *   Home Page con griglia prodotti "Masonry-style".
    *   Filtri per Categoria e Ordinamento (Prezzo, Novità, Vetrina).
    *   Dettaglio prodotto con galleria immagini, varianti (taglia/colore) e storie generate da AI.
    *   Carrello della spesa integrato.
*   **Pannello di Amministrazione**:
    *   Gestione completa prodotti (Aggiungi, Modifica, Elimina).
    *   Gestione Stock avanzata:
        *   **Prodotti Semplici**: Campo "Stock" dedicato per oggetti unici.
        *   **Prodotti con Varianti**: Gestione stock per ogni singola variante.
    *   **Gestione Categorie**: Strumento per rinominare o unire categorie (utile per rimuovere categorie errate come "Prova").
    *   **Priorità Vetrina**: Campo numerico per decidere l'ordine di apparizione dei prodotti.
    *   **Integrazione AI**: Generazione descrizioni e storie vintage.

## 🛠 Istruzioni Rapide

### 1. Rimuovere/Rinominare Categorie
Se vuoi eliminare una categoria (es. "Prova"):
1.  Vai nel **Pannello Admin** > **Configurazione Globale** (in alto).
2.  Sotto "Gestione Categorie", seleziona "Prova" dal menu a tendina.
3.  Nel campo a fianco, scrivi il nome della categoria corretta (es. "Tech Luxury") o un nuovo nome.
4.  Clicca **RINOMINA / UNISCI**.
5.  Tutti i prodotti "Prova" verranno spostati. Se la vecchia categoria non ha più prodotti, sparirà dai filtri.

### 2. Correggere Immagini Errate
Se un prodotto mostra una foto sbagliata nell'inventario:
1.  Clicca modifica (matita) sul prodotto.
2.  Verifica la sezione **Immagine Prodotto** (galleria principale).
3.  Verifica le **Varianti**: controlla se qualche variante ha una foto vecchia caricata.
4.  Se necessario, usa il tasto "Rimuovi tutte" sulle varianti o cancella l'URL dal campo principale e ricarica la foto corretta.
5.  Clicca **SALVA**.

### 3. Gestione Stock Semplice
Per prodotti senza taglie/colori:
1.  Nel form di modifica, assicurati di **NON avere varianti** (cancella tutte le righe varianti se presenti).
2.  Apparirà il campo **"Stock (Se senza varianti)"**.
3.  Inserisci lì la quantità (es. 5).
4.  Salva.

---

## 🔒 Sicurezza: Blindare il Database
Attualmente le regole di sicurezza di Firebase sono aperte (`allow read, write: if true;`). Per proteggere il negozio e impedire modifiche non autorizzate, devi aggiornare le regole nella Console di Firebase.

### Istruzioni Passo-Passo:
1.  Vai su [Firebase Console](https://console.firebase.google.com/).
2.  Apri il progetto **Boutique LM**.
3.  Nel menu a sinistra, vai su **Firestore Database** > Tab **Regole**.
4.  Cancella tutto e incolla questo codice (sostituendo `<TUO_ID_UTENTE_ADMIN>` se vuoi restrizioni specifiche per UID, altrimenti la regola auth generica va bene se sei l'unico utente registrato):

```firestore-security-rules
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Funzione helper per verificare se l'utente è loggato
    function isAuth() {
      return request.auth != null;
    }

    // Regola per i prodotti (Pubblici in lettura, Scrittura solo Admin)
    match /artifacts/{appId}/public/data/products/{productId} {
      allow read: if true;  // Chiunque può vedere i prodotti
      allow write: if isAuth(); // Solo utenti loggati (l'admin) possono modificare
    }

    // Regola per le impostazioni (Solo Admin)
    match /artifacts/{appId}/config/settings {
      allow read, write: if isAuth();
    }
    
    // Blocca tutto il resto di default
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
```

5.  Fai la stessa cosa per **Storage** (sezione Storage > Rules):

```firestore-security-rules
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /{allPaths=**} {
      allow read: if true; // Immagini visibili a tutti
      allow write: if request.auth != null; // Upload solo se loggati
    }
  }
}
```

### Nota Importante sull'Account Admin
Assicurati che **l'autenticazione Email/Password** sia attiva in Firebase Authentication e che tu abbia creato il tuo account admin (lo script di login nel sito usa `signInWithEmailAndPassword`). Queste regole proteggono il DB basandosi sul fatto che solo TU hai le credenziali di accesso.
