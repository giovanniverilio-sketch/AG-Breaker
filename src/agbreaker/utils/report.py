import json
from datetime import datetime
from pathlib import Path
from typing import Any

# Salva il risultato finale dell'attacco in un file JSON.
def save_report(
    output_path: str,
    target_file: str,
    file_type: str,
    attack_type: str,
    found: bool,
    password: str | None = None,
    attempts: int = 0,
) -> None:

    # Costruisce il dizionario contenente i dati dell'attacco
    report: dict[str, Any] = {
        "target_file": target_file,
        "file_type": file_type,
        "attack_type": attack_type,
        "found": found,
        "password": password if found else None,
        "attempts": attempts,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    # Converte il percorso di output in un oggetto Path
    path = Path(output_path)

    # Verifica se il file deve essere salvato in una sottocartella
    if path.parent != Path("."):
        # Crea le directory mancanti senza errore se esistono già
        path.parent.mkdir(parents=True, exist_ok=True)

    # Apre o crea il file JSON in modalità scrittura
    with path.open("w", encoding="utf-8") as file:
        # Converte il dizionario Python in JSON e lo salva nel file
        json.dump(report, file, indent=4, ensure_ascii=False) 
