import itertools
import sys

from agbreaker.cli import parse_args
from agbreaker.utils.checkpoint import delete_checkpoint, load_checkpoint, save_checkpoint
from agbreaker.utils.detector import detect_file_type
from agbreaker.utils.report import save_report

CHECKPOINT_SUFFIX = ".checkpoint.json"
CHECKPOINT_OGNI_N_TENTATIVI = 5000


def _checkpoint_path(output_path: str) -> str:
    return output_path + CHECKPOINT_SUFFIX


def _crea_cracker(file_type: str, filepath: str):
    if file_type == "zip":
        from agbreaker.core.zip_cracker import ZipCracker
        return ZipCracker(filepath)
    if file_type == "pdf":
        from agbreaker.core.pdf_cracker import PdfCracker
        return PdfCracker(filepath)
    raise ValueError(f"Formato non supportato: {file_type}")


def _prepara_candidati(args):
    if args.bruteforce:
        from agbreaker.attacks.bruteforce import bruteforce_attack
        return bruteforce_attack(args.charset, args.maxlen), "bruteforce"
    else:
        from agbreaker.attacks.dictionary import dictionary_attack
        return dictionary_attack(args.wordlist), "dictionary"


def main(argv=None) -> int:
    args = parse_args(argv)

    print("=========================================")
    print("      AG-BREAKER: PASSWORD RECOVERY      ")
    print("=========================================")

    file_type = detect_file_type(args.file)
    print(f"[*] Formato rilevato: {file_type.upper()}")

    cracker = _crea_cracker(file_type, args.file)
    candidati, tipo_attacco = _prepara_candidati(args)

    checkpoint_path = _checkpoint_path(args.output)
    tentativi_da_saltare = 0

    if args.resume:
        checkpoint = load_checkpoint(checkpoint_path)
        if checkpoint and checkpoint.get("target_file") == args.file:
            tentativi_da_saltare = checkpoint.get("attempts", 0)
            print(f"[*] Ripresa da checkpoint: {tentativi_da_saltare} tentativi già effettuati")
            candidati = itertools.islice(candidati, tentativi_da_saltare, None)
        else:
            print("[*] Nessun checkpoint valido trovato, riparto da zero")

    print(f"[*] Avvio attacco a {tipo_attacco} su {args.file}...")

    password_trovata = None
    tentativi = tentativi_da_saltare

    try:
        for candidato in candidati:
            tentativi += 1
            if cracker.prova_password(candidato):
                password_trovata = candidato
                break

            if tentativi % CHECKPOINT_OGNI_N_TENTATIVI == 0:
                save_checkpoint(
                    checkpoint_path,
                    {"target_file": args.file, "attack_type": tipo_attacco, "attempts": tentativi},
                )

    except KeyboardInterrupt:
        save_checkpoint(
            checkpoint_path,
            {"target_file": args.file, "attack_type": tipo_attacco, "attempts": tentativi},
        )
        print(f"\n[!] Interrotto dall'utente dopo {tentativi} tentativi.")
        print(f"[!] Checkpoint salvato in {checkpoint_path}. Riprendi con --resume.")
        return 130

    if password_trovata:
        print(f"[+] Password trovata: {password_trovata}")
        delete_checkpoint(checkpoint_path)
    else:
        print("[-] Nessuna password trovata")

    save_report(
        args.output,
        target_file=args.file,
        file_type=file_type,
        attack_type=tipo_attacco,
        found=password_trovata is not None,
        password=password_trovata,
        attempts=tentativi,
    )
    print(f"[*] Report salvato in {args.output}")

    return 0 if password_trovata else 1


if __name__ == "__main__":
    sys.exit(main())
