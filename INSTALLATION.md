# 👨🏻‍💻 Development
<!-- L'intero progetto è stato sviluppato su due macchine Apple:

- Sistema Operativo:  macOS Monterey 12.3.1.
- Architettura: Apple Silicon M1 (ARM).

Il progetto è stato eseguito correttamente anche su una macchina Windows 10 (x64). -->

The entire project was developed on two Apple 🍏 machines:

- Operating system: macOS Monterey 12.3.1.
- Architecture: Apple Silicon M1 (ARM).

The project ran successfully on a Windows 10 (x64) machine.


# ⚒ Installation
<!-- 
1. Installare o aggiornare all'ultima versione stabile di python dal sito: https://www.python.org/downloads/.

2. Verificare la corretta installazione di Python eseguendo i seguenti comandi: -->

1. Install or upgrade to the latest stable version of python from: https://www.python.org/downloads/.

2. Verify the correct installation of Python by running the following commands:

    ```bash

    python --version

    ```

    or

    ```bash

    python3 --version

    ```

<!-- 3. Verificare la corrette installazione (in bundle con Python) di Pip: -->

3. Verify the correct installation (bundled with Python) of PIP:

    ```bash

    pip --version

    ```

    or

    ```bash

    pip3 --version

    ```

<!-- 4. Spostarsi nella root del progetto (pyenv).

5. Installare le dipendenze richieste: -->

4. Move to the root of the project (pyenv).

5. Install the required dependencies:

    ```bash

    pip install -r requirements.txt

    ```

    or

    ```bash

    pip3 install -r requirements.txt
    ```

# 🔮 Usage

Run the following commands from the root of the project (pyenv).

1. Create the db

    ```bash

    python manage.py migrate

    ```

2. Running the server

    ```bash

    python manage.py runserver

    ```

Go to the address shown in cmd (it should be http://localhost:8000/).