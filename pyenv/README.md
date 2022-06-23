# Welcome to our awesome Bank!

## Gruppo

 - Calabrese Alex - Matr. 869054
 -  Lombardo Matteo - Matr. 869232

# Description
Abbiamo sfruttato l'occasione di questo progetto per poterci approcciare all'utilizzo di **Python** e **Django** in quanto, molto richiesti dal mercato, ma a noi sconosciuti.
Inoltre, è stato interessante gestire le dinamiche di lavoro di gruppo tra colleghi, grazie all'utilizzo di tool per il versioning del software (git).

## Scelte Progettuali

### Frontend (HTML, CSS, JS w/ VueJs)
- **Dipendenze**
	Per evitare ulteriori dipendenze, tutto il necessario per il Frontend è incluso utilizzando le **CDN**, motivo per cui, potrebbe esserci qualche piccola parte dell'interfaccia non stilizzata.
- **Aggiunte**
	- Per **comodità** nel reperire degli id e verificare la correttezza delle informazioni, senza doversi interfacciare direttamente con il database, all'interno della **homepage** (root del server): è stata aggiunta un'**ulteriore sezione** che comprende la **lista di tutti gli account registrati** con le relative informazioni.

### Backend (Python w/ Django)
Nei vari endpoints, sono stati aggiunti ulteriori campi, oltre quelli richiesti, per facilitare la lettura delle informazioni attraverso il frontend.

 - **Database**
	 Per memorizzare le informazioni è stato utilizzato un database **SQLite**.
 - **Depositi/Prelievi**
	I Depositi/Prelievi sono stati modellati con una apposita tabella "selftransaction" per differenziarli dal concetto di Transazione.
 -  **Account Eliminati**
	- La tabella "account" prevede il campo **"is_active"** che indica se l'account è attivo, oppure "eliminato" (utilizzando l'endpoint DELETE "/api/account").
	- Ovviamente, le parti del sistema che visualizzano/gestiscono gli accounts, non avranno visibilità sugli account eliminati (is_active = 0).
	- Inoltre, all'atto dell'eliminazione di un account, il suo **id** continuerà ad essere presente nello storico delle transazioni, per preservare l'integrità delle stesse.
 - **Transazioni Annullate (diverted)**
	- La tabella "transaction" prevede il campo **"is_diverted"** che indica se la transazione è stata annullata (utilizzando l'endpoint POST "/api/divert").
	- L'annullamento di una transazione è un'operazione effettuabile **una sola volta**.
	- Nel caso in cui, uno dei due account coinvolti nella transazione che si vuole annullare dovessero essere stati eliminati, non sarà possibile annullare quella transazione.
