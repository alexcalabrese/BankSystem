
# Welcome to our awesome Bank! 💸

  

# 👨🏻‍💻 Group

- Alex Calabrese | [LinkedIn](https://www.linkedin.com/in/alex-calabrese)
- Matteo Lombardo

  

# 📜 Description

> ⚠️
> This is a project created for **Distributed System** exam.

> 🏆
> Score: ***30 with honors*** / 30.

We took the opportunity of this project to be able to approach the use of **Python** and **Django** as, highly demanded by the market, but unknown to us.

In addition, it was interesting to manage the dynamics of group work among colleagues by using software versioning tools.

If you want to run on your machine ➡️ **[Installation](/INSTALLATION.md)**.

<!-- Abbiamo sfruttato l'occasione di questo progetto per poterci approcciare all'utilizzo di **Python** e **Django** in quanto, molto richiesti dal mercato, ma a noi sconosciuti. -->
<!-- 
Inoltre, è stato interessante gestire le dinamiche di lavoro di gruppo tra colleghi, grazie all'utilizzo di tool per il versioning del software (git). -->

  
<!-- ## Scelte Progettuali -->

# 🎨 Design Choices
   
- **[Frontend](#frontend)**
- **[Backend](#backend)**
  

## <a name="frontend"></a> 🖌 &nbsp; Frontend
Framework:  **Vuejs**.

### 🍂 &nbsp; **Dependencies**

To avoid additional dependencies, everything needed for the Frontend is included using **CDNs**, which is why there may be some small part of the interface that is not stylized.

<!-- Per evitare ulteriori dipendenze, tutto il necessario per il Frontend è incluso utilizzando le **CDN**, motivo per cui, potrebbe esserci qualche piccola parte dell'interfaccia non stilizzata. -->

### ➕ &nbsp; **Additions**

For **convenience** in retrieving ids and verifying the correctness of the information, without having to interface directly with the database, within the **homepage** (server root): an **additional section** has been added that includes the **list of all registered accounts** with related information.

<!-- Per **comodità** nel reperire degli id e verificare la correttezza delle informazioni, senza doversi interfacciare direttamente con il database, all'interno della **homepage** (root del server): è stata aggiunta un'**ulteriore sezione** che comprende la **lista di tutti gli account registrati** con le relative informazioni. -->

  

## <a name="backend"></a> 🐍 Backend 

Framework: **Python w/ Django**.

<!-- Nei vari endpoints, sono stati aggiunti ulteriori campi, oltre quelli richiesti, per facilitare la lettura delle informazioni attraverso il frontend. -->

  

### 🗃 &nbsp; **Database**

To store the information, **SQLite** database is used.

<!-- Per memorizzare le informazioni è stato utilizzato un database **SQLite**. -->

### 💳 &nbsp; **Deposits/Withdrawals**

Deposits/Withdrawals are modelled with a special "_selfTransaction_" table to distinguish them from the "_Transaction_" concept.

<!-- I Depositi/Prelievi sono stati modellati con una apposita tabella "selftransaction" per differenziarli dal concetto di Transazione. -->

### ❌ &nbsp; **Deleted Accounts** 

- The "_account_" table provides the **"is_active"** field indicating whether the account is active, or "_deleted_" (using the DELETE "/api/account" endpoint).

<!-- - La tabella "account" prevede il campo **"is_active"** che indica se l'account è attivo, oppure "eliminato" (utilizzando l'endpoint DELETE "/api/account"). -->

- Obviously, the parts of the system that view/manage accounts, will have no visibility into deleted accounts (_is_active = 0_).

<!-- - Ovviamente, le parti del sistema che visualizzano/gestiscono gli accounts, non avranno visibilità sugli account eliminati (is_active = 0). -->

- When an account is deleted, its **id** will continue to be present in the transaction history to **preserve the integrity of transactions**.

<!-- - Inoltre, all'atto dell'eliminazione di un account, il suo **id** continuerà ad essere presente nello storico delle transazioni, per preservare l'integrità delle stesse. -->

### ❌ &nbsp; **Cancelled Transactions (diverted)**

- The "_transaction_" table provides the **"is_diverted"** field that indicates whether the transaction has been cancelled (using the POST endpoint "/api/divert").

<!-- - La tabella "transaction" prevede il campo **"is_diverted"** che indica se la transazione è stata annullata (utilizzando l'endpoint POST "/api/divert"). -->

- Cancelling a transaction is a **one-time** operation.

<!-- - L'annullamento di una transazione è un'operazione effettuabile **una sola volta**. -->

- In case, one of the two accounts involved in the transaction you want to cancel should have been *deleted*, you will not be able to cancel that transaction.

<!-- - Nel caso in cui, uno dei due account coinvolti nella transazione che si vuole annullare dovessero essere stati eliminati, non sarà possibile annullare quella transazione. -->
