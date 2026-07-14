# Scelte progettuali — AG-Breaker

## 1. Obiettivo del documento

Questo documento raccoglie le principali scelte progettuali fatte durante lo sviluppo di AG-Breaker.

L'obiettivo non è ripetere il manuale utente o il manuale tecnico, ma spiegare perché il progetto è stato organizzato in un certo modo, quali alternative sono state considerate e quali compromessi sono stati accettati.

Le scelte principali riguardano:

* struttura del progetto;
* uso dell'ereditarietà;
* separazione dei moduli;
* gestione degli attacchi;
* rilevamento del formato dei file;
* salvataggio del report;
* gestione del checkpoint;
* scelta delle librerie esterne.

---

## 2. Struttura del progetto

Il progetto è stato organizzato usando una struttura con cartella `src/`.

```text
AG-Breaker/
├── src/
│   └── agbreaker/
├── tests/
├── docs/
├── README.md
└── requirements.txt
```

Questa scelta permette di separare chiaramente:

* codice sorgente;
* test;
* documentazione;
* file di configurazione del progetto.

La cartella `src/agbreaker` contiene il pacchetto Python vero e proprio. In questo modo il codice è più ordinato e risulta più semplice distinguere ciò che fa parte dell'applicazione da ciò che serve solo per test, documentazione o configurazione.

Una struttura piatta, con tutti i file Python nella root del progetto, sarebbe stata più semplice all'inizio, ma meno ordinata e meno adatta a un progetto da presentare e difendere all'orale.

---

## 3. Separazione in moduli

Il codice è stato diviso in tre aree principali:

```text
core/
attacks/
utils/
```

### `core/`

Contiene le classi principali del progetto:

* `Cracker`;
* `ZipCracker`;
* `PdfCracker`.

Questa cartella rappresenta il cuore logico del programma, cioè la parte che sa provare una password su un file protetto.

### `attacks/`

Contiene i generatori di password candidate:

* attacco a dizionario;
* attacco brute force.

Questa scelta separa la generazione delle password dalla verifica della password.

In questo modo il codice che genera le password non deve sapere se il file è ZIP o PDF.

### `utils/`

Contiene funzioni di supporto:

* rilevamento formato;
* report JSON;
* checkpoint.

Queste funzionalità non appartengono direttamente né alla gerarchia dei cracker né agli attacchi, quindi sono state isolate in moduli separati.

---

## 4. Scelta dell'ereditarietà

La scelta più importante del progetto è l'uso dell'ereditarietà nella gerarchia:

```text
Cracker
├── ZipCracker
└── PdfCracker
```

Questa scelta è giustificata perché esiste una relazione reale di tipo "is-a":

```text
ZipCracker è un Cracker
PdfCracker è un Cracker
```

Entrambe le sottoclassi rappresentano un tipo specifico di cracker. Hanno in comune il fatto che ricevono un file protetto e provano password candidate, ma differiscono nel modo concreto in cui verificano la password.

Per questo motivo è stata creata una classe base astratta `Cracker`, che definisce il comportamento comune e obbliga le sottoclassi a implementare il metodo:

```python
prova_password(password: str) -> bool
```

Il metodo `prova_password()` è polimorfico: viene chiamato dal resto del programma senza sapere se l'oggetto concreto è uno `ZipCracker` o un `PdfCracker`.

Esempio concettuale:

```python
cracker.prova_password("password123")
```

Il codice che chiama questo metodo non deve conoscere il formato specifico del file. Sarà l'oggetto concreto a decidere quale implementazione eseguire.

---

## 5. Perché non usare solo funzioni

Un'alternativa possibile era usare semplici funzioni separate:

```python
prova_password_zip(file, password)
prova_password_pdf(file, password)
```

Questa soluzione sarebbe stata più semplice all'inizio, ma avrebbe reso più difficile estendere il programma.

Con funzioni separate, il motore principale avrebbe dovuto controllare continuamente il tipo di file:

```python
if file_type == "zip":
    prova_password_zip(...)
elif file_type == "pdf":
    prova_password_pdf(...)
```

Questo approccio funziona con due formati, ma diventa meno ordinato quando si aggiungono nuovi formati.

Con l'ereditarietà, invece, il programma lavora con un oggetto generico di tipo `Cracker` e chiama sempre lo stesso metodo:

```python
cracker.prova_password(password)
```

Questa scelta rende il codice più estendibile e più coerente con la programmazione orientata agli oggetti.

---

## 6. Perché non usare solo composizione

Un'altra alternativa era usare la composizione, creando una classe principale che contenesse strategie diverse per ZIP e PDF.

La composizione sarebbe stata una scelta valida se il comportamento fosse stato costruito combinando più oggetti indipendenti.

In AG-Breaker, però, `ZipCracker` e `PdfCracker` non sono componenti generici da inserire dentro un'altra classe. Sono davvero due specializzazioni dello stesso concetto: un cracker di file protetti.

Per questo motivo l'ereditarietà è più naturale.

La domanda di controllo è:

```text
ZipCracker è un Cracker?
PdfCracker è un Cracker?
```

La risposta è sì. Quindi la relazione di ereditarietà è coerente.

---

## 7. Uso di `super().__init__()`

Le sottoclassi `ZipCracker` e `PdfCracker` chiamano il costruttore della classe base usando:

```python
super().__init__(filepath)
```

Questa scelta evita duplicazione di codice.

La validazione comune del percorso del file viene fatta una sola volta nella classe base `Cracker`.

In questo modo non è necessario riscrivere in ogni sottoclasse controlli come:

* il file esiste?
* il percorso punta davvero a un file?
* il percorso va salvato come attributo dell'oggetto?

Le sottoclassi possono concentrarsi solo sulla logica specifica del formato.

---

## 8. Scelta di `pyzipper` per i file ZIP

Per i file ZIP è stata scelta la libreria `pyzipper`.

Una prima alternativa possibile era usare il modulo standard `zipfile` di Python. Tuttavia `zipfile` ha limiti nella gestione di alcuni archivi cifrati, in particolare quelli con cifratura AES.

`pyzipper` è più adatta allo scopo del progetto perché permette di lavorare meglio con archivi ZIP protetti da password.

Questa scelta è coerente con l'obiettivo di supportare casi più realistici rispetto a un esempio minimo.

---

## 9. Scelta di `pikepdf` per i file PDF

Per i file PDF è stata scelta la libreria `pikepdf`.

L'obiettivo non è modificare il contenuto del PDF, ma tentare l'apertura del documento usando una password candidata.

`pikepdf` permette di aprire PDF protetti e gestire l'errore quando la password non è corretta.

In questo modo `PdfCracker.prova_password()` può rispettare la stessa interfaccia di `ZipCracker.prova_password()`:

```python
True se la password è corretta
False se la password è errata
```

---

## 10. Generatori per dizionario e brute force

Le funzioni di attacco sono state implementate come generatori.

Questo significa che producono una password alla volta usando `yield`.

La scelta è importante soprattutto per l'attacco a dizionario: una wordlist può contenere milioni di righe e non sarebbe efficiente caricarla tutta in memoria.

Approccio scelto:

```python
for password in dictionary_attack(path):
    ...
```

In questo modo il programma legge una riga, prova la password, poi passa alla successiva.

Anche il brute force viene gestito come generatore, perché il numero di combinazioni può crescere molto rapidamente.

Questo approccio permette di:

* ridurre il consumo di memoria;
* interrompere l'attacco appena viene trovata la password;
* integrare più facilmente progress bar e checkpoint.

---

## 11. Rilevamento formato tramite magic bytes

Per riconoscere il tipo di file è stata scelta la lettura dei magic bytes, cioè i primi byte del file.

Questa scelta è più affidabile rispetto al controllo dell'estensione.

Un file potrebbe chiamarsi:

```text
documento.pdf
```

ma non essere realmente un PDF.

I formati gestiti sono:

```text
ZIP → PK
PDF → %PDF
```

Il modulo `detector.py` ha quindi il compito di leggere l'inizio del file e stabilire se il formato è supportato.

---

## 12. Report JSON

Il risultato finale dell'attacco viene salvato in un file JSON.

JSON è stato scelto perché:

* è leggibile;
* è semplice da generare in Python;
* può essere aperto facilmente da altri programmi;
* si adatta bene a dati strutturati.

Il report può contenere:

* file analizzato;
* formato;
* tipo di attacco;
* password trovata;
* numero di tentativi;
* data di creazione.

Questo rende il risultato dell'esecuzione persistente, non limitato solo all'output del terminale.

---

## 13. Checkpoint

Il checkpoint è stato previsto per salvare lo stato di avanzamento di un attacco.

Questa scelta è utile perché alcuni attacchi possono richiedere molto tempo. Senza checkpoint, un'interruzione costringerebbe l'utente a ricominciare da zero.

Il checkpoint può salvare informazioni come:

* file bersaglio;
* tipo di attacco;
* ultima password provata;
* numero di tentativi.

L'obiettivo è permettere una ripresa tramite opzione:

```text
--resume
```

Questa funzionalità aumenta l'utilità pratica del progetto, anche se richiede attenzione per mantenere coerente lo stato salvato.

---

## 14. Gestione delle eccezioni

Nel progetto è importante distinguere tra:

* password sbagliata;
* errore reale del programma.

Una password sbagliata non deve essere trattata come un crash. Deve semplicemente produrre:

```python
False
```

Un errore reale, invece, può essere:

* file inesistente;
* file corrotto;
* formato non supportato;
* wordlist mancante;
* permessi insufficienti.

Questa distinzione rende il programma più robusto e più chiaro per l'utente.

---

## 15. Compromessi accettati

Il progetto non vuole essere un'alternativa completa a strumenti professionali di password recovery.

Sono stati accettati alcuni compromessi:

* supporto limitato a ZIP e PDF;
* brute force pensato per casi piccoli o didattici;
* nessun supporto iniziale a GPU o parallelizzazione;
* nessuna interfaccia grafica;
* focus su chiarezza, testabilità e architettura OOP.

Questi compromessi sono coerenti con il contesto del corso e con il tempo disponibile.

---

## 16. Possibili estensioni future

L'architettura permette diverse estensioni:

* aggiunta di `RarCracker`;
* supporto a nuovi formati;
* parallelizzazione degli attacchi;
* statistiche sui tentativi;
* esportazione del report in CSV;
* interfaccia più avanzata;
* miglioramento del checkpoint;
* progress bar più dettagliata;
* test su file reali di esempio.

La gerarchia basata su `Cracker` facilita queste estensioni, perché ogni nuovo formato può essere aggiunto come nuova sottoclasse.

---

## 17. Sintesi

Le scelte progettuali principali di AG-Breaker sono state fatte per ottenere un progetto:

* modulare;
* leggibile;
* estendibile;
* testabile;
* coerente con la programmazione orientata agli oggetti.

La scelta dell'ereditarietà è centrale perché rappresenta correttamente la relazione tra la classe base `Cracker` e le sue sottoclassi `ZipCracker` e `PdfCracker`.

Il metodo polimorfico `prova_password()` permette al resto del programma di lavorare con formati diversi usando un'interfaccia comune.
