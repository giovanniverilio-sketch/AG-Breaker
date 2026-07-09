import sys
from src.agbreaker.cli import parse_args

def main():
    # Sfrutta il parser creato in cli.py
    args = parse_args()

    print("\n=========================================")
    print("      AG-BREAKER: PASSWORD RECOVERY      ")
    print("=========================================\n")
    print(f"[*] Target selezionato: {args.file}")
    print(f"[*] Report finale programmato in: {args.output}")

    # Validazione logica dei parametri prima di invocare i motori d'attacco
    if not args.wordlist and not args.bruteforce:
        print("[-] Errore: Devi specificare una modalità d'attacco.")
        print("    Usa --wordlist <path> oppure attiva --bruteforce.")
        sys.exit(1)

    if args.wordlist and args.bruteforce:
        print("[-] Errore: Modalità ambigua. Scegli o solo --wordlist o solo --bruteforce.")
        sys.exit(1)

    # Placeholder per l'integrazione con i moduli di Persona 2
    if args.wordlist:
        print(f"[*] Avvio pianificato: Attacco a dizionario con {args.wordlist}...")
        # Qui si inserirà la chiamata al dizionario
    elif args.bruteforce:
        print(f"[*] Avvio pianificato: Brute Force (Lunghezza massima: {args.maxlen})...")
        # Qui si inserirà la chiamata al brute force

if __name__ == "__main__":
    main()