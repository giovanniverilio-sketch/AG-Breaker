from pathlib import Path

SUPPORTED_FORMATS = {"zip", "pdf"}

# Funzione per rilevare il tipo di file in base al contenuto del file
def detect_file_type(filepath: str) -> str:
    path = Path(filepath)

    if not path.exists(): # verifica se il percorso esiste
        raise FileNotFoundError(f"File non trovato: {filepath}")

    if not path.is_file(): # verifica se il percorso è un file valido
        raise ValueError(f"Il percorso non è un file valido: {filepath}")

    with path.open("rb") as file: # apre il file in modalità binaria per leggere i primi 8 byte
        header = file.read(8)

    if header.startswith(b"PK"): # verifica se il file è un file ZIP controllando i primi due byte
        return "zip"

    if header.startswith(b"%PDF"): # verifica se il file è un file PDF controllando i primi 4 byte
        return "pdf"

    # Se il file non è né ZIP né PDF, solleva un'eccezione
    raise ValueError("Formato file non supportato. Sono supportati solo ZIP e PDF.")

# Funzione per verificare se il file è supportato
def is_supported_file(filepath: str) -> bool:
    try:
        detect_file_type(filepath)
        return True
    except (FileNotFoundError, ValueError):
        return False
