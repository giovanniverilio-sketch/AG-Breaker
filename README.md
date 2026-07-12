# AG-Breaker

Tool da riga di comando per il recupero di password su file cifrati (ZIP e PDF)
tramite attacco a dizionario o brute force.
> Il progetto è pensato esclusivamente per uso legittimo su file propri, ambienti di laboratorio o challenge CTF autorizzate.

Progetto finale Programmazione Python — corso CYSS
Autori: Abdelrahman Zaher — Giovanni Verilio.

---

## Cosa fa

Il programma prova automaticamente password candidate su un file ZIP o PDF protetto.
Supporta due modalità di attacco:

- **Dizionario** — legge le password da una wordlist (es. rockyou.txt)
- **Brute force** — genera tutte le combinazioni possibili dato un charset e una lunghezza massima

Quando trova la password corretta la mostra a schermo e salva un report JSON con il risultato.

---

## Requisiti

- Python 3.11+
- pip

---

## Installazione

```bash
git clone https://github.com/giovanniverilio-sketch/AG-Breaker
cd AG-Breaker
pip install -r requirements.txt
```

---

## Avvio rapido

Mostrare l'help del programma:

```bash
python -m agbreaker --help
```

Esempio di comando base con attacco a dizionario:

```bash
python -m agbreaker --file esempi/archivio.zip --wordlist wordlists/passwords.txt --output report.json
```

> Nota: i comandi definitivi potranno essere aggiornati durante lo sviluppo, in base alla struttura finale della CLI.

---

## Utilizzo

### Attacco a dizionario su un file ZIP

```bash
python -m agbreaker --file esempi/archivio.zip --wordlist wordlists/passwords.txt --output report.json
```

### Attacco a dizionario su un file PDF

```bash
python -m agbreaker --file esempi/documento.pdf --wordlist wordlists/passwords.txt --output report.json
```

### Brute force

```bash
python -m agbreaker --file esempi/archivio.zip --bruteforce --charset abc123 --maxlen 4 --output report.json
```

### Visualizzare l'help

```bash
python -m agbreaker --help
```

### Tutte le opzioni

| Opzione        | Descrizione                                               | Default         |
|----------------|-----------------------------------------------------------|-----------------|
| `--file`       | Percorso del file da craccare (ZIP o PDF)                 | obbligatorio    |
| `--wordlist`   | Percorso della wordlist per attacco a dizionario          | —               |
| `--bruteforce` | Attiva la modalità brute force                            | disattivo       |
| `--charset`    | Caratteri da usare nel brute force                        | a-z + 0-9       |
| `--maxlen`     | Lunghezza massima della password nel brute force          | 4               |
| `--output`     | Percorso del report JSON                                  | `report.json`   |
| `--resume`     | Riprende una sessione interrotta usando il checkpoint      | disattivo       |

---

## Esempio di output

```
[*] Formato rilevato: ZIP
[*] Avvio attacco a dizionario su archivio.zip...
[*] Parole caricate: 14344392
100%|████████████████████████| 14344392/14344392 [00:43<00:00]
[+] Password trovata: batman123
[*] Report salvato in report.json
```

---

## Struttura del progetto

```text
AG-Breaker/
├── README.md
├── requirements.txt
├── .gitignore
├── docs/
│   ├── proposta.md
│   ├── manuale-utente.md
│   ├── manuale-tecnico.md
│   ├── scelte.md
│   ├── uso-ia.md
│   └── devlog.md
├── src/
│   └── agbreaker/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── cracker.py
│       │   ├── zip_cracker.py
│       │   └── pdf_cracker.py
│       ├── attacks/
│       │   ├── __init__.py
│       │   ├── dictionary.py
│       │   └── bruteforce.py
│       └── utils/
│           ├── __init__.py
│           ├── report.py
│           ├── checkpoint.py
│           └── detector.py
└── tests/
    ├── test_bruteforce_attack.py
    ├── test_cracker_base.py
    ├── test_detector.py
    ├── test_dictionary_attack.py
    └── test_polymorphism.py
```
---

## Eseguire i test

Per eseguire i test unitari del progetto:

```bash
pytest tests/
```
I test servono a verificare che le parti principali del programma funzionino correttamente, in particolare:

* la classe base `Cracker`;
* il comportamento delle sottoclassi `ZipCracker` e `PdfCracker`;
* l'attacco a dizionario;
* il polimorfismo del metodo `prova_password()`.

Durante lo sviluppo i test devono essere eseguiti spesso, soprattutto dopo modifiche alla logica degli attacchi o alla gerarchia delle classi.

---

## Documentazione

```text
docs/
├── proposta.md
├── manuale-utente.md
├── manuale-tecnico.md
├── scelte.md
├── uso-ia.md
└── devlog.md
```

Contenuto dei documenti:

* `proposta.md`: proposta approvata dal docente e punto di partenza del progetto;
* `manuale-utente.md`: guida per installare e usare AG-Breaker da riga di comando;
* `manuale-tecnico.md`: spiegazione dell'architettura interna, dei moduli e della gerarchia di classi;
* `scelte.md`: motivazione delle scelte progettuali, inclusa la scelta dell'ereditarietà;
* `uso-ia.md`: dichiarazione trasparente sull'uso di strumenti di intelligenza artificiale;
* `devlog.md`: diario di sviluppo del gruppo, con problemi incontrati, decisioni prese e avanzamento del lavoro.

---

## Stato del progetto

Il progetto è attualmente in fase di sviluppo.

Funzionalità già previste:

- struttura iniziale del repository;
- documentazione nella cartella `docs/`;
- classe base astratta `Cracker`;
- supporto per file ZIP e PDF;
- attacco a dizionario;
- attacco brute force;
- report JSON;
- checkpoint di sessione;
- test unitari con `pytest`.

Le funzionalità verranno implementate progressivamente seguendo il piano approvato nella proposta.

---

## Autori

- Abdelrahman Zaher
- Giovanni Verilio
