import pyzipper

from agbreaker.core.cracker import Cracker


class ZipCracker(Cracker):
    """Cracker specializzato per archivi ZIP (ZipCrypto e AES)."""

    def __init__(self, filepath: str):
        # super().__init__() riusa la validazione comune della classe base
        # (il file deve esistere ed essere un file vero e proprio).
        super().__init__(filepath)

    def prova_password(self, password: str) -> bool:
        try:
            with pyzipper.AESZipFile(self.filepath) as zip_file:
                zip_file.pwd = password.encode("utf-8")
                file_list = zip_file.namelist()

                if not file_list:
                    return False

                # Basta un file corretto per confermare la password: non
                # serve estrarre tutto l'archivio.
                zip_file.read(file_list[0])
                return True

        except RuntimeError:
            # Password errata: pyzipper solleva RuntimeError in questo caso.
            return False
        except pyzipper.BadZipFile:
            return False
        except pyzipper.LargeZipFile:
            return False
        except Exception:
            # Rete di sicurezza: un tentativo fallito non deve mai far
            # crashare un attacco che magari sta girando da ore su milioni
            # di candidati.
            return False
