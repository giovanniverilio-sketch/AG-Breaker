from abc import ABC, abstractmethod
from pathlib import Path


class Cracker(ABC):
    def __init__(self, filepath: str):

        path = Path(filepath)

        if not path.exists():
            raise FileNotFoundError(f"File non trovato: {filepath}")

        if not path.is_file():
            raise ValueError(f"Il percorso non è un file valido: {filepath}")

        self.filepath = filepath

    @abstractmethod
    def prova_password(self, password: str) -> bool:

        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(filepath={self.filepath!r})"
