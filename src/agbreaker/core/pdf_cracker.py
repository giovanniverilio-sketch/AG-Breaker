from pathlib import Path
import pikepdf
from agbreaker.core.cracker import Cracker

"""
Cracker specifico per file PDF protetti da password. 
Estende la classe astratta Cracker e implementa il metodo prova_password per verificare se una password è corretta per un file PDF.
"""
class PdfCracker(Cracker):

    # Inizializza il PdfCracker con il percorso del file PDF da attaccare.
    def __init__(self, filepath: str):
        super().__init__(filepath)

        path = Path(filepath)

        if not path.exists():
            raise FileNotFoundError(f"File PDF non trovato: {filepath}")

        if not path.is_file():
            raise ValueError(f"Il percorso non è un file valido: {filepath}")

    # Prova una password sul file PDF protetto. Restituisce True se la password è corretta, altrimenti False.
    def prova_password(self, password: str) -> bool:

        try:
            with pikepdf.open(self.filepath, password=password):
                return True
            
        except pikepdf.PasswordError:# Se la password è errata, cattura l'eccezione PasswordError e restituisce False
            return False
        
        except pikepdf.PdfError: # Se il file PDF è corrotto o non può essere aperto, cattura l'eccezione PdfError e restituisce False
            return False
