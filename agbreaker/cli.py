import argparse

def parse_args():
    """
    Configura e gestisce gli argomenti passati da riga di comando.
    """
    parser = argparse.ArgumentParser(
        prog="agbreaker",
        description="AG-Breaker: Strumento didattico per il recupero password di file ZIP e PDF."
    )

    # Argomento obbligatorio
    parser.add_argument(
        "-f", "--file", 
        required=True, 
        help="Percorso del file ZIP o PDF da analizzare"
    )

    # Modalità di attacco (mutuamente esclusive in logica, ma gestite via codice)
    parser.add_argument(
        "-w", "--wordlist", 
        help="Percorso del file di testo (wordlist) per l'attacco a dizionario"
    )
    parser.add_argument(
        "-b", "--bruteforce", 
        action="store_true", 
        help="Attiva la modalità di generazione combinazioni (brute force)"
    )

    # Parametri aggiuntivi per il brute force
    parser.add_argument(
        "-c", "--charset", 
        default="abcdefghijklmnopqrstuvwxyz0123456789", 
        help="Insieme di caratteri da usare nel brute force (Default: a-z + 0-9)"
    )
    parser.add_argument(
        "-m", "--maxlen", 
        type=int, 
        default=4, 
        help="Lunghezza massima della password da tentare nel brute force (Default: 4)"
    )

    # Output e gestione sessione
    parser.add_argument(
        "-o", "--output", 
        default="report.json", 
        help="Percorso del file JSON in cui salvare il report finale (Default: report.json)"
    )
    parser.add_argument(
        "-r", "--resume", 
        action="store_true", 
        help="Riprende un attacco interrotto dall'ultimo checkpoint salvato"
    )

    return parser.parse_args()