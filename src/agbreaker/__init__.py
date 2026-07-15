from agbreaker.core.cracker import Cracker

__all__ = ["Cracker", "ZipCracker", "PdfCracker"]


def __getattr__(name: str):
    if name == "ZipCracker":
        from agbreaker.core.zip_cracker import ZipCracker
        return ZipCracker
    if name == "PdfCracker":
        from agbreaker.core.pdf_cracker import PdfCracker
        return PdfCracker
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
