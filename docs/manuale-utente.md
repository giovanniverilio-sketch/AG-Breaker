# Manuale utente — AG-Breaker

## 1. Introduzione

AG-Breaker è un tool da riga di comando scritto in Python per tentare il recupero della password di file protetti.

Il programma supporta due formati principali:

* file ZIP;
* file PDF.

Il recupero della password può essere tentato con due modalità:

* attacco a dizionario;
* attacco brute force.

Il progetto è pensato per uso didattico, per esercitazioni di laboratorio, per challenge CTF autorizzate e per il recupero di password dimenticate su file propri.

> AG-Breaker deve essere usato solo su file propri o in ambienti dove si ha autorizzazione esplicita. L'uso su file di terzi senza permesso non è consentito.

---

## 2. Requisiti

Per usare AG-Breaker servono:

* Python 3.11 o superiore;
* pip;
* sistema operativo Windows, Linux o macOS;
* terminale o prompt dei comandi.

Le dipendenze Python sono indicate nel file:

```text
requirements.txt
```

Le librerie principali usate dal progetto sono:

* `pyzipper`, per la gestione di archivi ZIP cifrati;
* `pikepdf`, per la gestione di PDF protetti da password;
* `tqdm`, per mostrare una barra di avanzamento;
* `pytest`, per eseguire i test del progetto.

---

## 3. Installazione

Clonare il repository GitHub:

```bash
git clone https://github.com/giovanniverilio-sketch/AG-Breaker.git
```

Entrare nella cartella del progetto:

```bash
cd AG-Breaker
```

Installare le dipendenze:

```bash
pip install -r requirements.txt
```

Se si usa Windows e il comando `pip` non funziona, provare:

```bash
python -m pip install -r requirements.txt
```

---

## 4. Avvio del programma

Il programma è pensato per essere avviato da riga di comando.

Comando per visualizzare l'help:

```bash
python -m agbreaker --help
```

Se il progetto non è ancora installato come pacchetto e viene usata la struttura `src/`, durante lo sviluppo può essere necessario eseguire:

### Windows PowerShell

```powershell
$env:PYTHONPATH="src"
python -m agbreaker --help
```

### Linux/macOS

```bash
PYTHONPATH=src python -m agbreaker --help
```

L'help mostra le opzioni disponibili e permette di verificare che il programma venga avviato correttamente.

---

## 5. Opzioni principali

| Opzione        | Descrizione                                                         |
| -------------- | ------------------------------------------------------------------- |
| `--file`       | Percorso del file ZIP o PDF da analizzare                           |
| `--wordlist`   | Percorso della wordlist da usare per l'attacco a dizionario         |
| `--bruteforce` | Attiva la modalità brute force                                      |
| `--charset`    | Indica i caratteri da usare nel brute force                         |
| `--maxlen`     | Indica la lunghezza massima delle password generate nel brute force |
| `--output`     | Percorso del file JSON dove salvare il report finale                |
| `--resume`     | Riprende una sessione interrotta tramite checkpoint, se disponibile |

---

## 6. Attacco a dizionario

L'attacco a dizionario usa una lista di password candidate, chiamata wordlist.

Ogni riga del file viene letta come una possibile password. Il programma prova le password una alla volta finché:

* trova la password corretta;
* finisce la wordlist;
* l'utente interrompe l'esecuzione.

Esempio su file ZIP:

```bash
python -m agbreaker --file esempi/archivio.zip --wordlist wordlists/passwords.txt --output report.json
```

Esempio su file PDF:

```bash
python -m agbreaker --file esempi/documento.pdf --wordlist wordlists/passwords.txt --output report.json
```

Durante lo sviluppo, se il pacchetto non viene trovato, usare:

```bash
PYTHONPATH=src python -m agbreaker --file esempi/archivio.zip --wordlist wordlists/passwords.txt --output report.json
```

Su Windows PowerShell:

```powershell
$env:PYTHONPATH="src"
python -m agbreaker --file esempi/archivio.zip --wordlist wordlists/passwords.txt --output report.json
```

---

## 7. Attacco brute force

L'attacco brute force genera automaticamente tutte le combinazioni possibili a partire da un insieme di caratteri.

Esempio:

```bash
python -m agbreaker --file esempi/archivio.zip --bruteforce --charset abc123 --maxlen 4 --output report.json
```

In questo caso il programma genera password usando solo i caratteri:

```text
a b c 1 2 3
```

fino a una lunghezza massima di 4 caratteri.

Esempi di password generate:

```text
a
b
c
1
2
3
aa
ab
ac
...
```

Il brute force può diventare molto lento se il charset è grande o se la lunghezza massima è alta.

Esempio:

```text
charset = abcdefghijklmnopqrstuvwxyz0123456789
maxlen = 6
```

produce un numero molto elevato di combinazioni.

Per questo motivo, durante i test, conviene usare charset piccoli e lunghezze basse.

---

## 8. Report JSON

Quando l'attacco termina, AG-Breaker salva un report in formato JSON.

Il report può contenere informazioni come:

* file analizzato;
* tipo di file rilevato;
* tipo di attacco usato;
* password trovata, se presente;
* numero di tentativi effettuati;
* data e ora di creazione del report.

Esempio semplificato:

```json
{
    "target_file": "archivio.zip",
    "file_type": "zip",
    "attack_type": "dictionary",
    "found": true,
    "password": "batman123",
    "attempts": 1250,
    "created_at": "2026-07-14T15:30:00"
}
```

Il percorso del report può essere scelto con l'opzione:

```bash
--output report.json
```

---

## 9. Checkpoint e ripresa

AG-Breaker prevede un sistema di checkpoint per salvare lo stato di avanzamento di una sessione.

Questo è utile quando:

* l'attacco richiede molto tempo;
* l'utente interrompe il programma;
* si vuole riprendere in seguito senza ricominciare da zero.

Per riprendere una sessione interrotta si usa l'opzione:

```bash
--resume
```

Esempio:

```bash
python -m agbreaker --file esempi/archivio.zip --wordlist wordlists/passwords.txt --resume
```

---

## 10. Esempio di esecuzione

Esempio di output del programma:

```text
[*] Formato rilevato: ZIP
[*] Avvio attacco a dizionario su archivio.zip
[*] Wordlist caricata: wordlists/passwords.txt
100%|████████████████████████| 1200/1200 [00:03<00:00]
[+] Password trovata: batman123
[*] Report salvato in report.json
```

Se la password non viene trovata, il programma mostra un messaggio simile:

```text
[-] Password non trovata
[*] Report salvato in report.json
```

---

## 11. Esecuzione dei test

Per eseguire i test unitari del progetto:

```bash
python -m pytest
```

Oppure:

```bash
python -m pytest tests/
```

Se il pacchetto `agbreaker` non viene trovato, impostare `PYTHONPATH`.

Windows PowerShell:

```powershell
$env:PYTHONPATH="src"
python -m pytest
```

Linux/macOS:

```bash
PYTHONPATH=src python -m pytest
```

---

## 12. Errori comuni

### ModuleNotFoundError: No module named 'agbreaker'

Questo errore indica che Python non trova il pacchetto `agbreaker`.

Durante lo sviluppo, risolvere impostando `PYTHONPATH`.

Windows PowerShell:

```powershell
$env:PYTHONPATH="src"
python -m pytest
```

Linux/macOS:

```bash
PYTHONPATH=src python -m pytest
```

### FileNotFoundError

Questo errore compare quando il percorso del file indicato non esiste.

Controllare:

* che il file ZIP o PDF esista davvero;
* che il percorso sia scritto correttamente;
* che ci si trovi nella cartella giusta del progetto.

### Formato file non supportato

AG-Breaker supporta solo file ZIP e PDF.

Se viene passato un file diverso, il programma deve rifiutarlo e mostrare un errore chiaro.
