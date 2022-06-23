
# Instructions
## Installing
1. Installare o aggiornare all'ultima versione stabile di python dal sito: https://www.python.org/downloads/.
2. Verificare la corretta installazione di Python eseguendo i seguenti comandi:
	```bash
	python --version
	```
	oppure
	```bash
	python3 --version
	```
3. Verificare la corrette installazione (in bundle con Python) di Pip:
	```bash
	pip --version
	```
	oppure
	```bash
	pip3 --version
	 ```
4. Spostarsi nella root del progetto (pyenv).
5. Installare le dipendenze richieste:
	```bash
	pip install -r requirements.txt
	```
	oppure
	```bash
	pip3 install -r requirements.txt
	```
	
### Usage
Eseguire i seguenti comandi dalla root del progetto (pyenv).
1. Creare il db
```bash
python manage.py migrate
```
3. Eseguire il server
```bash
python manage.py runserver
```

Recarsi all'indirizzo mostrato nel cmd (dovrebbe essere http://127.0.0.1:8000/)
