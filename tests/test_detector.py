from pathlib import Path

import pytest

from agbreaker.utils.detector import detect_file_type, is_supported_file


def test_detect_file_type_zip(tmp_path: Path):
    zip_file = tmp_path / "test.zip"
    zip_file.write_bytes(b"PK\x03\x04contenuto")

    assert detect_file_type(str(zip_file)) == "zip"


def test_detect_file_type_pdf(tmp_path: Path):
    pdf_file = tmp_path / "test.pdf"
    pdf_file.write_bytes(b"%PDF-1.7 contenuto")

    assert detect_file_type(str(pdf_file)) == "pdf"


def test_detect_file_type_unsupported(tmp_path: Path):
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("ciao", encoding="utf-8")

    with pytest.raises(ValueError):
        detect_file_type(str(txt_file))


def test_is_supported_file(tmp_path: Path):
    pdf_file = tmp_path / "test.pdf"
    pdf_file.write_bytes(b"%PDF-1.7 contenuto")

    assert is_supported_file(str(pdf_file)) is True