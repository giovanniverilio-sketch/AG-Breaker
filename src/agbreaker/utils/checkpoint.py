import json
from pathlib import Path
from typing import Any

# Salva i dati del checkpoint in un file JSON.
def save_checkpoint(checkpoint_path: str, data: dict[str, Any]) -> None:
    path = Path(checkpoint_path)

    # Verifica se il file deve essere salvato in una sottocartella e crea le directory mancanti senza errore se esistono già
    if path.parent != Path("."):
        path.parent.mkdir(parents=True, exist_ok=True)
    # Apre o crea il file JSON in modalità scrittura e salva i dati del checkpoint
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Carica i dati del checkpoint da un file JSON.
def load_checkpoint(checkpoint_path: str) -> dict[str, Any] | None:
    path = Path(checkpoint_path)

    # controlla se il file esiste, se non esiste restituisce None
    if not path.exists():
        return None

    # Apre il file JSON in modalità lettura e carica i dati del checkpoint
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)

# Elimina il file di checkpoint se esiste.
def delete_checkpoint(checkpoint_path: str) -> None:
    path = Path(checkpoint_path)
    
    # Controlla se il file esiste e lo elimina
    if path.exists():
        path.unlink()
