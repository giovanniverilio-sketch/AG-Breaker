# Devlog — AG-Breaker

## Entry 1 — Avvio progetto e proposta

**Data:** [inserire data reale]

In questa prima fase abbiamo analizzato la richiesta del progetto finale e scelto l'idea di AG-Breaker, un tool da riga di comando per tentare il recupero di password su file ZIP e PDF.

Abbiamo deciso di proporre un progetto legato alla sicurezza informatica perché è coerente con il nostro percorso e perché ha un'utilità concreta in contesti didattici, CTF e recupero di file personali.

La parte più importante da progettare fin dall'inizio è stata la gerarchia di classi richiesta dal docente. Abbiamo scelto una classe base astratta `Cracker` e due sottoclassi, `ZipCracker` e `PdfCracker`.

Il metodo polimorfico principale previsto è `prova_password()`: il resto del programma può chiamare questo metodo senza sapere se il file analizzato è uno ZIP o un PDF.

Abbiamo anche definito le funzionalità principali:

* attacco a dizionario;
* attacco brute force;
* rilevamento automatico del formato;
* report JSON;
* checkpoint per riprendere una sessione interrotta;
* test unitari con `pytest`.

In questa fase abbiamo capito che il progetto non doveva essere solo uno script unico, ma un programma organizzato in moduli, con responsabilità separate e difendibile all'orale.

---

## Entry 2 — Creazione repository e struttura iniziale

**Data:** [inserire data reale]

Dopo l'approvazione della proposta, abbiamo creato il repository GitHub pubblico del progetto e impostato la struttura iniziale.

Abbiamo scelto una struttura con cartella `src/`, separando il codice sorgente dalla documentazione e dai test.

La struttura principale è:

```text
src/agbreaker/
├── core/
├── attacks/
├── utils/
├── cli.py
└── __main__.py
```

Abbiamo creato anche le cartelle:

```text
docs/
tests/
```

In `docs/` abbiamo inserito la proposta approvata e creato i file richiesti per la documentazione:

* `manuale-utente.md`;
* `manuale-tecnico.md`;
* `scelte.md`;
* `uso-ia.md`;
* `devlog.md`.

In `tests/` abbiamo preparato i file per i test unitari.

Durante questa fase abbiamo avuto alcune difficoltà con GitHub e con i permessi di push, perché il repository era stato creato dall'account di un membro del gruppo. Abbiamo risolto aggiungendo l'altro membro come collaboratore e verificando l'accesso al repository.

Abbiamo anche capito l'importanza di fare commit piccoli e chiari, invece di un unico commit finale.

---

## Entry 3 — Divisione del lavoro e primi moduli

**Data:** [inserire data reale]

Abbiamo diviso il lavoro in due blocchi principali.

Il primo blocco riguarda il core e l'interfaccia:

* classe base `Cracker`;
* sottoclasse `ZipCracker`;
* CLI con `argparse`;
* file `__main__.py`;
* test della gerarchia base;
* manuale utente.

Il secondo blocco riguarda i motori di attacco e le utility:

* `PdfCracker`;
* generatore dizionario;
* generatore brute force;
* rilevamento formato file;
* report JSON;
* checkpoint;
* manuale tecnico.

Questa divisione ci ha aiutato a lavorare in parallelo senza modificare continuamente gli stessi file.

Abbiamo deciso di usare `pyzipper` per i file ZIP e `pikepdf` per i PDF, perché queste librerie sono più adatte allo scopo del progetto rispetto ad alternative più generiche.

In questa fase abbiamo iniziato a scrivere i generatori di password. Per l'attacco a dizionario abbiamo scelto di usare `yield`, così la wordlist viene letta riga per riga senza caricarla tutta in memoria.

Per il brute force abbiamo scelto `itertools.product`, perché permette di generare combinazioni in modo semplice e leggibile.

---

## Entry 4 — Problemi incontrati e correzioni

**Data:** [inserire data reale]

Durante lo sviluppo abbiamo incontrato alcuni problemi pratici.

Uno dei primi problemi è stato l'errore:

```text
ModuleNotFoundError: No module named 'agbreaker'
```

Questo errore era causato dalla struttura con cartella `src/`: eseguendo direttamente un file di test, Python non trovava automaticamente il pacchetto `agbreaker`.

Abbiamo capito che i test devono essere eseguiti dalla root del progetto usando `pytest`, eventualmente impostando `PYTHONPATH=src` durante lo sviluppo.

Un altro problema è stato legato a Git: in alcuni momenti il branch locale risultava indietro rispetto al repository remoto. Abbiamo usato `git pull --rebase origin main` per integrare i commit remoti prima di fare push.

Abbiamo anche notato che alcuni file richiedevano una correzione della formattazione, perché il codice deve essere leggibile, indentato correttamente e compatibile con Python.

Questa fase è stata utile perché ci ha fatto capire che non basta scrivere codice: bisogna anche controllare che il progetto parta da clone pulito, che i test siano eseguibili e che la struttura sia coerente.

---

## Entry 5 — Documentazione e preparazione alla revisione

**Data:** [inserire data reale]

In questa fase abbiamo iniziato a completare la documentazione nella cartella `docs/`.

Abbiamo lavorato su:

* manuale utente;
* manuale tecnico;
* scelte progettuali;
* uso dell'intelligenza artificiale;
* devlog.

Nel manuale utente abbiamo spiegato come installare il progetto, come avviarlo da terminale e come usare le principali opzioni.

Nel manuale tecnico abbiamo documentato l'architettura interna, i moduli principali e la gerarchia di classi.

Nel file `scelte.md` abbiamo spiegato perché abbiamo usato l'ereditarietà: `ZipCracker` e `PdfCracker` sono entrambi tipi specifici di `Cracker`, quindi la relazione "is-a" è coerente.

Nel file `uso-ia.md` abbiamo dichiarato un uso moderato dell'intelligenza artificiale come supporto per chiarimenti, revisione, Git e organizzazione della documentazione.

Il prossimo passo sarà correggere i file Python uno per uno, verificare gli import, sistemare eventuali errori di formattazione ed eseguire tutti i test con `pytest`.

L'obiettivo finale è arrivare a un progetto che si possa clonare, installare e avviare seguendo il README senza interventi manuali aggiuntivi.
