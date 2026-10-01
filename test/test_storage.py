
import os
import csv
from src.storage import uloz_vysledek 
SOUBOR = "outputs/history.csv"

testovaci_vysledek = {
    "url": "https://vatican.va",
    "is_online": True,
    "status_code": 200,
    "response_time_ms": 342,
    "checked_at": "2026-05-19 10:00:00",
    "page_size_kb": 45.2,
    "ssl_valid": True,
    "ssl_expires_in_days": 145
}

def test_soubor_se_vytvori():
    uloz_vysledek(testovaci_vysledek)
    assert os.path.exists(SOUBOR)

def test_hlavicka_existuje():
    uloz_vysledek(testovaci_vysledek)
    with open(SOUBOR, "r", encoding="utf-8-sig") as soubor:
        reader = csv.reader(soubor)
        radek = next(reader)
        assert "url" in radek

def test_data_se_ulozi():
    uloz_vysledek(testovaci_vysledek)
    with open(SOUBOR, "r", encoding="utf-8-sig") as soubor:
        reader = csv.reader(soubor)
        radek = next(reader)
        nalezene_url = []
        for radek in reader:
            if radek:
                nalezene_url.append(radek[0])
        assert "https://vatican.va" in nalezene_url

def test_pocet_sloupcu():
    uloz_vysledek(testovaci_vysledek)
    with open(SOUBOR, "r", encoding="utf-8-sig") as soubor:
        reader = csv.reader(soubor)
        next(reader)
        radek = next(reader)
        assert len(radek) == 8

def test_none_nespadne():
    uloz_vysledek(None)
    

