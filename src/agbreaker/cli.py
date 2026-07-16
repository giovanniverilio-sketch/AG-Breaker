import argparse


def crea_parser() -> argparse.ArgumentParser:
    """Costruisce il parser degli argomenti di AG-Breaker."""
    parser = argparse.ArgumentParser(
        prog="agbreaker",
        description="AG-Breaker: strumento didattico per il recupero password di file ZIP e PDF.",
    )

    parser.add_argument(
        "-f", "--file",
        required=True,
        help="Percorso del file ZIP o PDF da analizzare.",
    )
    parser.add_argument(
        "-w", "--wordlist",
        help="Percorso del file di testo (wordlist) per l'attacco a dizionario.",
    )
    parser.add_argument(
        "-b", "--bruteforce",
        action="store_true",
        help="Attiva la modalità brute force al posto del dizionario.",
    )
    parser.add_argument(
        "-c", "--charset",
        default="abcdefghijklmnopqrstuvwxyz0123456789",
        help="Caratteri da usare nel brute force (default: a-z + 0-9).",
    )
    parser.add_argument(
        "-m", "--maxlen",
        type=int,
        default=4,
        help="Lunghezza massima della password nel brute force (default: 4).",
    )
    parser.add_argument(
        "-o", "--output",
        default="report.json",
        help="Percorso del file JSON in cui salvare il report finale (default: report.json).",
    )
    parser.add_argument(
        "-r", "--resume",
        action="store_true",
        help="Riprende un attacco interrotto dall'ultimo checkpoint salvato.",
    )

    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parsa argv e valida le combinazioni di opzioni.

    Args:
        argv: lista di argomenti. Se None, argparse usa sys.argv (comportamento
            normale da riga di comando). Passare una lista esplicita è utile
            nei test, per non dipendere da sys.argv.

    Returns:
        Namespace con gli argomenti validati.
    """
    parser = crea_parser()
    args = parser.parse_args(argv)

    if not args.wordlist and not args.bruteforce:
        parser.error("specificare --wordlist oppure --bruteforce")

    if args.wordlist and args.bruteforce:
        parser.error("--wordlist e --bruteforce sono mutuamente esclusivi")

    if args.maxlen <= 0:
        parser.error("--maxlen deve essere un intero positivo")

    if args.bruteforce and not args.charset:
        parser.error("--charset non può essere vuoto in modalità brute force")

    return args
