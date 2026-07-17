from pathlib import Path

import pikepdf
import pyzipper
import pytest

from agbreaker.core.cracker import Cracker
from agbreaker.core.pdf_cracker import PdfCracker
from agbreaker.core.zip_cracker import ZipCracker


def _crea_zip_protetto(path: Path, password: str) -> None:
    with pyzipper.AESZipFile(
        path, "w", compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES
    ) as zf:
        zf.setpassword(password.encode("utf-8"))
        zf.writestr("segreto.txt", "contenuto di prova")


def _crea_pdf_protetto(path: Path, password: str) -> None:
    pdf = pikepdf.new()
    pdf.save(str(path), encryption=pikepdf.Encryption(owner="owner_pw", user=password))


def prova_password_su_lista(crackers: list[Cracker], password: str) -> list[bool]:
    """Funzione "cliente" che non sa nulla delle sottoclassi concrete:
    riceve una lista eterogenea di Cracker e chiama prova_password() su
    ognuno esattamente allo stesso modo. È questa la dimostrazione del
    polimorfismo: il comportamento cambia in base al tipo concreto, ma il
    codice chiamante resta identico."""
    return [c.prova_password(password) for c in crackers]


def test_zip_e_pdf_cracker_sono_entrambi_sottoclassi_di_cracker():
    assert issubclass(ZipCracker, Cracker)
    assert issubclass(PdfCracker, Cracker)


def test_polimorfismo_su_lista_eterogenea_di_cracker(tmp_path: Path):
    zip_path = tmp_path / "archivio.zip"
    pdf_path = tmp_path / "documento.pdf"

    _crea_zip_protetto(zip_path, "batman123")
    _crea_pdf_protetto(pdf_path, "batman123")

    crackers: list[Cracker] = [
        ZipCracker(str(zip_path)),
        PdfCracker(str(pdf_path)),
    ]

    # Stessa password corretta per entrambi: la funzione cliente non fa
    # alcuna distinzione fra ZIP e PDF, eppure il risultato è corretto
    # per entrambi grazie all'override di prova_password() in ciascuna
    # sottoclasse.
    risultati = prova_password_su_lista(crackers, "batman123")
    assert risultati == [True, True]


def test_polimorfismo_con_password_sbagliata(tmp_path: Path):
    zip_path = tmp_path / "archivio.zip"
    pdf_path = tmp_path / "documento.pdf"

    _crea_zip_protetto(zip_path, "correcthorse")
    _crea_pdf_protetto(pdf_path, "correcthorse")

    crackers: list[Cracker] = [
        ZipCracker(str(zip_path)),
        PdfCracker(str(pdf_path)),
    ]

    risultati = prova_password_su_lista(crackers, "password_sbagliata")
    assert risultati == [False, False]


def test_metodo_prova_password_e_ridefinito_in_ogni_sottoclasse():
    """Verifica che l'override sia reale (non ereditato "per pigrizia"
    dalla classe base, cosa impossibile qui essendo astratta, ma utile
    come check esplicito di leggibilità del codice)."""
    assert ZipCracker.prova_password is not Cracker.prova_password
    assert PdfCracker.prova_password is not Cracker.prova_password
    assert ZipCracker.prova_password is not PdfCracker.prova_password
