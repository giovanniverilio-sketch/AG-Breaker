from collections.abc import Generator 
from pathlib import Path 

# una funzione che legge un file di wordlist e restituisce le password una alla volta come generator
def dictionary_attack(wordlist_path: str) -> Generator[str, None, None]: 
    path = Path(wordlist_path) # Converte il percorso in un oggetto Path

    # Verificare che il percorso sia valido
    if not path.exists(): 
        raise FileNotFoundError(f"Wordlist non trovata: {wordlist_path}")
    if not path.is_file():
        raise ValueError(f"Il percorso specificato non è un file: {wordlist_path}")
    
    #Aprire il file e leggere le password riga per riga
    with path.open("r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            password = line.strip()
            if password: 
                yield password # Restituisce una password alla volta 