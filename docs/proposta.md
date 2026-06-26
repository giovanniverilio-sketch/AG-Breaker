# AG-Breaker — Password Cracker Multi-Formato

**Gruppo:** Abdelrahman Zaher — Giovanni Verilio  
**Data:** 26 giugno 2026

---

## 1. Cosa fa il programma

Il programma è un tool da riga di comando che tenta di recuperare la password di file protetti
tramite attacco a dizionario o brute force. L'utente fornisce il file bersaglio, sceglie il tipo
di attacco e, se usa il dizionario, fornisce una wordlist. Il tool prova automaticamente tutte
le password candidate e quando trova quella corretta la mostra a schermo e salva il risultato
in un report JSON. Supporta più formati di file (ZIP e PDF), mostra una progress bar durante
l'attacco e permette di configurare charset e lunghezza massima per il brute force. In caso di
interruzione salva il punto di avanzamento per riprendere la sessione in seguito.

---

## 2. A chi serve e quale problema reale risolve

Il tool è utile in due scenari concreti:

- **CTF (Capture The Flag):** nelle competizioni di sicurezza informatica capita spesso di
  trovare file ZIP o PDF protetti da password come parte di una sfida. Avere uno strumento
  dedicato e configurabile è un vantaggio pratico immediato.
- **Recupero password dimenticate:** chi ha un file importante di cui non ricorda più la
  password può usare il tool per tentarne il recupero, senza dover ricorrere a software
  commerciali o online.

Il programma è anche uno strumento didattico per capire concretamente perché le password
corte o comuni sono pericolose.

---

## 3. Competenze del corso messe in gioco

| Competenza | Come viene usata |
|---|---|
| OOP ed ereditarietà | gerarchia di cracker, polimorfismo sul metodo `prova_password()` |
| File I/O | lettura wordlist, lettura file bersaglio, salvataggio report e checkpoint |
| Hashing | uso di `hashlib` per alcuni confronti interni |
| CLI con `argparse` | interfaccia a riga di comando con opzioni configurabili |
| JSON | salvataggio report risultati e checkpoint di sessione |
| Gestione eccezioni | distinguere "password sbagliata" da errori reali |

---

## 4. Gerarchia di ereditarietà

```
Cracker  (classe base astratta)
│
├── CrackerZIP   → apre archivi ZIP cifrati con pyzipper
└── CrackerPDF   → apre PDF protetti da password con pikepdf
```

**Classe base `Cracker`:**

La classe base raccoglie tutto il comportamento comune ai due cracker. Contiene gli attributi
condivisi — il percorso del file bersaglio (`filepath`), la wordlist da usare nell'attacco a
dizionario (`wordlist`), il charset e la lunghezza massima per il brute force — e i metodi che
orchestrano l'attacco: `attacca_dizionario()` e `attacca_bruteforce()`. Entrambi i metodi
funzionano allo stesso modo indipendentemente dal formato: generano le password candidate
una per una e chiamano `prova_password()`.

**Metodo polimorfico — `prova_password(pwd: str) -> bool`:**

Questo è il cuore dell'ereditarietà. È dichiarato astratto nella classe base e ogni sottoclasse
lo ridefinisce con la propria logica:

- `CrackerZIP.prova_password()` tenta di aprire l'archivio con `pyzipper` usando la password fornita
- `CrackerPDF.prova_password()` tenta di aprire il PDF con `pikepdf` usando la password fornita

Il motore di attacco non sa mai quale formato sta trattando: chiama soltanto `prova_password()`
e aspetta un `True` o `False`. Questo è polimorfismo reale — aggiungere un `CrackerRAR` domani
non richiederebbe toccare il motore.

**Uso di `super().__init__()`:**

Ogni sottoclasse chiama `super().__init__()` per inizializzare gli attributi comuni (`filepath`,
`wordlist`, ecc.) prima di aggiungere i propri attributi specifici, evitando duplicazione di codice.

---

## 5. Piano di massima in fasi

**Fase 1 — Fondamenta (giorni 1–5) → metà percorso**
- Struttura repo: `src/`, `docs/`, `tests/`, `requirements.txt`, README base
- Classe base `Cracker` con metodo astratto `prova_password()`
- `CrackerZIP` funzionante con attacco a dizionario
- Primi test unitari

*A metà percorso: tool funzionante su ZIP con dizionario, repo strutturato, test verdi.*

**Fase 2 — Espansione (giorni 6–12)**
- `CrackerPDF` con attacco a dizionario
- Brute force configurabile (charset, lunghezza massima)
- Progress bar con `tqdm`
- Salvataggio checkpoint per sessioni interrotte
- Report JSON

**Fase 3 — Documentazione e rifinitura (giorni 13–18)**
- Manuale utente, manuale tecnico, `scelte.md`, `uso-ia.md`, devlog completo
- Test aggiuntivi su edge case e polimorfismo
- Verifica avvio da clone pulito

**Fase 4 — Preparazione orale (giorni 19–20)**
- Code review reciproca: entrambi devono saper spiegare tutto
- Ripasso gerarchia di classi
