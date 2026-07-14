import pyzipper
from agbreaker.core.cracker import Cracker
"""
Cracker specifico per file ZIP protetti da password. 
Estende la classe astratta Cracker e implementa il metodo prova_password per verificare se una password è corretta per un file ZIP.
"""
class ZipCracker(Cracker):

    # Inizializza il ZipCracker con il percorso del file ZIP da attaccare.
    def __init__(self, filepath: str):
        super().__init__(filepath)

    # Prova una password sul file ZIP protetto. Restituisce True se la password è corretta, altrimenti False.
    def prova_password(self, password: str) -> bool:
        try:
            with pyzipper.AESZipFile(self.filepath) as zip_file:
                password_bytes = password.encode("utf-8")
                zip_file.pwd = password_bytes
                file_list = zip_file.namelist()

                if not file_list: # Se il file ZIP è vuoto, restituisce False
                    return False

                first_file = file_list[0]
                zip_file.read(first_file)

                return True 

        except RuntimeError: # Se la password è errata, cattura l'eccezione RuntimeError e restituisce False
            return False
        except pyzipper.BadZipFile: # Se il file ZIP è corrotto o non può essere aperto, cattura l'eccezione BadZipFile e restituisce False
            return False
        except pyzipper.LargeZipFile: # Se il file ZIP è troppo grande, cattura l'eccezione LargeZipFile e restituisce False
            return False
        except Exception: # Cattura qualsiasi altra eccezione e restituisce False
            return False
