import pytest
from agbreaker.attacks.bruteforce import bruteforce_attack

def test_bruteforce_attack_generates_combinations():
    passwords = list(bruteforce_attack("ab", 2))
    assert passwords == ["a", "b", "aa", "ab", "ba", "bb"]

def test_bruteforce_attack_empty_charset():
    with pytest.raises(ValueError):
        list(bruteforce_attack("", 3))

def test_bruteforce_attack_invalid_length():
    with pytest.raises(ValueError):
        list(bruteforce_attack("abc", 0))