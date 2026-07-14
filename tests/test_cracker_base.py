from pathlib import Path
import pyzipper
import pytest
from agbreaker.core.cracker import Cracker
from agbreaker.core.zip_cracker import ZipCracker

# Funzione di utilità per creare un file ZIP protetto da password per i test.
def create_test_zip(zip_path: Path, password: str) -> None:

    # Crea un file ZIP protetto da password con un file di testo di prova all'interno.
    with pyzipper.AESZipFile(
        zip_path,
        "w",
        compression=pyzipper.ZIP_DEFLATED,
        encryption=pyzipper.WZ_AES,
    ) as zip_file:
        zip_file.setpassword(password.encode("utf-8"))
        zip_file.writestr("test.txt", "contenuto di prova")

# Test per verificare il comportamento della classe astratta Cracker e della classe concreta ZipCracker.
def test_cracker_is_abstract():

    with pytest.raises(TypeError):
        Cracker("file.zip")

# Test per verificare che ZipCracker possa essere istanziato correttamente e che erediti da Cracker.
def test_zip_cracker_instance(tmp_path: Path):

    zip_path = tmp_path / "archivio.zip"
    create_test_zip(zip_path, "password123")

    cracker = ZipCracker(str(zip_path))

    assert isinstance(cracker, ZipCracker)
    assert isinstance(cracker, Cracker)
    assert cracker.filepath == str(zip_path)

# Test per verificare che ZipCracker sollevi FileNotFoundError se il file ZIP non esiste.
def test_zip_cracker_file_not_found():
    """
    Verifica che ZipCracker sollevi FileNotFoundError
    se il file indicato non esiste.
    """
    with pytest.raises(FileNotFoundError):
        ZipCracker("file_che_non_esiste.zip")

# Test per verificare che ZipCracker sollevi ValueError se il percorso non è un file valido.
def test_zip_cracker_correct_password(tmp_path: Path):
    """
    Verifica che prova_password() restituisca True
    quando la password dello ZIP è corretta.
    """
    zip_path = tmp_path / "archivio.zip"
    create_test_zip(zip_path, "password123")

    cracker = ZipCracker(str(zip_path))

    assert cracker.prova_password("password123") is True

# Test per verificare che ZipCracker restituisca False quando la password dello ZIP è sbagliata.
def test_zip_cracker_wrong_password(tmp_path: Path):
    """
    Verifica che prova_password() restituisca False
    quando la password dello ZIP è sbagliata.
    """
    zip_path = tmp_path / "archivio.zip"
    create_test_zip(zip_path, "password123")

    cracker = ZipCracker(str(zip_path))

    assert cracker.prova_password("admin") is False
