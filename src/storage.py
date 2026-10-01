
import csv
import os

SOUBOR = "outputs/history.csv"


def uloz_vysledek(vysledek):
    if vysledek is None:
        return
    os.makedirs("outputs", exist_ok=True)
    soubor_existuje = os.path.exists(SOUBOR)
    with open(SOUBOR, "a", encoding="utf-8", newline="") as soubor:
        writer = csv.writer(soubor)
        if not soubor_existuje:
            writer.writerow(["url", "is_online", "status_code", "response_time_ms", "checked_at", "page_size_kb", "ssl_valid", "ssl_expires_in_days"])
        writer.writerow(vysledek.values())
