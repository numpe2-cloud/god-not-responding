



from src.checker import zkontroluj_web

def test_vysledek_je_slovnik():
    vysledek = zkontroluj_web("https://google.com")
    assert isinstance(vysledek, dict)
    assert  "is_online" in vysledek

def test_response_time_je_cislo():
    vysledek = zkontroluj_web("https://google.com")
    assert isinstance(vysledek["response_time_ms"], (int, float))
    assert vysledek["response_time_ms"] > 0

def test_neplatna_url():
    vysledek = zkontroluj_web("https://toto-neexistuje-vubec-123456.cz")
    assert not vysledek["is_online"]

def test_status_code_pri_chybe():
     vysledek = zkontroluj_web("https://toto-neexistuje-vubec-123456.cz")
     assert vysledek["status_code"] is None