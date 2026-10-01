
import os
import yaml
import logging
from datetime import datetime
from src.checker import zkontroluj_web
from src.storage import uloz_vysledek
from src.reporter import generuj_dashboard

os.makedirs("outputs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
     handlers=[
        logging.FileHandler("outputs/monitor.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)


with open("config.yaml", encoding="UTF-8") as soubor:
    config = yaml.safe_load(soubor)
logging.info("Config načten")
cas_spusteni = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for server in config["weby"]:
    logging.info(f"Kontroluji: {server['url']}")
    vysledek = zkontroluj_web(server["url"], cas_spusteni)
    uloz_vysledek(vysledek)
    logging.info(f"Web je: {vysledek["is_online"]}")
generuj_dashboard()
logging.info("Dashboard byl vygenerován")