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
                file_list = []

                for file_info in zip_file.infolist():
                    if not file_info.is_dir():
                        file_list.append(file_info)

                if not file_list:
                    return False

                for file_info in file_list:
                    if file_info.flag_bits & 0x1:
                        zip_file.read(file_info.filename)
                        return True

                return False

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
