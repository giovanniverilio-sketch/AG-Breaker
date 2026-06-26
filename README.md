# AG-Breaker

Tool da riga di comando per il recupero di password su file cifrati (ZIP e PDF)
tramite attacco a dizionario o brute force.

Progetto finale — Corso di Programmazione Python (CYS)
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

```bash
....Coming Soon....
```

---

## Utilizzo

### Attacco a dizionario su un file ZIP

```bash
....Coming Soon....
```

### Attacco a dizionario su un file PDF

```bash
....Coming Soon....
```

### Brute force

```bash
....Coming Soon....
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

```
....Coming Soon....

```

---

## Eseguire i test

```bash
pytest tests/
```

---

## Documentazione

Tutta la documentazione si trova nella cartella `docs/`:

```
....Coming Soon....

```

---

## Autori

- Abdelrahman Zaher
- Giovanni Verilio
