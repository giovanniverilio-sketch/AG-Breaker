from collections.abc import Generator
from itertools import product

#Genera password brute force
def bruteforce_attack(charset: str, max_length: int) -> Generator[str, None, None]:

    # Verifica che il charset contenga almeno un carattere
    if not charset:
        raise ValueError("Il charset non può essere vuoto.")
    
    # Verifica che la lunghezza massima sia valida
    if max_length < 1:
        raise ValueError("La lunghezza massima deve essere almeno 1.")
    
    # Genera tutte le combinazioni di caratteri fino alla lunghezza massima
    for length in range(1, max_length + 1):
        for combination in product(charset, repeat=length):
            yield "".join(combination) #converte la tupla in stringa e la restituisce come password generata
