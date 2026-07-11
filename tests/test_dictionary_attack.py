from pathlib import Path
import pytest
from agbreaker.attacks.dictionary import dictionary_attack

# Crea un file di wordlist temporaneo e verifica che le password vengano lette correttamente
def test_dictionary_attack_reads_passwords(tmp_path: Path): 
    wordlist = tmp_path / "wordlist.txt" 
    wordlist.write_text("admin\npassword123\n\nciao\n", encoding="utf-8") # Scrive password e una riga vuota nel file
    passwords = list(dictionary_attack(str(wordlist))) 
    assert passwords == ["admin", "password123", "ciao"] # Verifica password e rimozione delle righe vuote

# Verifica che venga sollevata l'eccezione corretta quando il file non esiste
def test_dictionary_attack_file_not_found(): 
    with pytest.raises(FileNotFoundError):
        list(dictionary_attack("file_che_non_esiste.txt"))