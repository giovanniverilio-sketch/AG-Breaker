from abc import ABC, abstractmethod
from pathlib import Path
"""
Classe astratta per i cracker di file protetti da password. 
Definisce l'interfaccia comune per tutti i cracker specifici di tipo di file.
"""
class Cracker(ABC):

    # Inizializza il cracker con il percorso del file da attaccare.
    def __init__(self, filepath: str):
        path = Path(filepath)

        if not path.exists(): # se il file non esiste, solleva un'eccezione FileNotFoundError
            raise FileNotFoundError(f"File non trovato: {filepath}")

        if not path.is_file(): # se il percorso non è un file valido, solleva un'eccezione ValueError
            raise ValueError(f"Il percorso non è un file valido: {filepath}")

        self.filepath = filepath # salva il percorso del file da attaccare come attributo dell'istanza

    @abstractmethod # indica che il metodo deve essere implementato dalle sottoclassi

    # Prova una password sul file protetto. Deve essere implementato dalle sottoclassi specifiche per ogni tipo di file.
    def prova_password(self, password: str) -> bool:
        pass
