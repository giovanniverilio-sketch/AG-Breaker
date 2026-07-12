import pytest
from agbreaker.attacks.bruteforce import bruteforce_attack

# Verifica che la funzione generi correttamente tutte le combinazioni di caratteri fino alla lunghezza massima
def test_bruteforce_attack_generates_combinations():
    passwords = list(bruteforce_attack("ab", 2))
    assert passwords == ["a", "b", "aa", "ab", "ba", "bb"]

# Verifica che venga sollevata l'eccezione corretta quando il charset è vuoto
def test_bruteforce_attack_empty_charset():
    with pytest.raises(ValueError):
        list(bruteforce_attack("", 3))

# Verifica che venga sollevata l'eccezione corretta quando la lunghezza massima è negativa
def test_bruteforce_attack_invalid_length():
    with pytest.raises(ValueError):
        list(bruteforce_attack("abc", 0))
