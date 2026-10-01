[![Test, lint and publish image](https://github.com/numpe2-cloud/god-not-responding/actions/workflows/testy.yml/badge.svg)](https://github.com/numpe2-cloud/god-not-responding/actions/workflows/testy.yml)
# god-not-responding

> Gods never sleep, but sometimes their servers do.

Monitoruje dostupnost webů 12 vybraných náboženství a duchovních směrů.
Pravidelně testuje každý web, měří odezvu, kontroluje SSL certifikát,
počítá velikost stránky a generuje HTML dashboard s výsledky.

> Existuje i rozšířená verze tohoto projektu — [god-not-responding-monitoring](https://github.com/numpe2-cloud/god-not-responding-monitoring),
> která běží nepřetržitě ve smyčce na vlastním homelabu (Docker, docker-compose) a exportuje metriky
> do Prometheu, odkud se dají sledovat v živém Grafana dashboardu.

![Dashboard preview](dashboard_preview.png)

## Spuštění v Dockeru

Kontejner jednou zkontroluje všechny weby, zapíše výsledky a skončí.
Výsledky zůstanou na disku ve složce `outputs/` díky volume v `docker-compose.yaml`.

```bash
docker compose up --build
```

Hotový image je i na Docker Hubu:

```bash
docker pull hovnoprdelstetky/god-not-responding:latest
docker run --rm -v "$(pwd)/outputs:/app/outputs" hovnoprdelstetky/god-not-responding:latest
```

## Spuštění bez Dockeru

```bash
pip install -r requirements.txt
python main.py
```

## CI/CD

Při každém pushi na `master` spustí GitHub Actions testy (`pytest`) a kontrolu stylu (`flake8`)
na Pythonu 3.10 a 3.11. Když projdou, sestaví Docker image a nahraje ho na Docker Hub.

## Sledované weby

| Web | Náboženství |
|-----|-------------|
| vatican.va | katolická církev |
| islam.com | islám |
| vhp.org | hinduismus |
| dalailama.com | buddhismus |
| zen-buddhism.net | zen buddhismus |
| chabad.org | judaismus |
| sikhs.org | sikhismus |
| scientology.org | scientologie |
| thesatanictemple.com | satanismus |
| jw.org | Svědkové Jehovovi |
| spaghettimonster.org | Církev létajícího špagetového monstra |
| dudeism.com | dudeismus |

## Co se sleduje

| Metrika | Popis |
|---------|-------|
| `is_online` | je server dostupný? |
| `status_code` | HTTP status kód |
| `response_time_ms` | rychlost odpovědi v ms |
| `ssl_valid` | platný HTTPS certifikát? |
| `ssl_expires_in_days` | za kolik dní vyprší SSL |
| `page_size_kb` | velikost stránky v kB |
| `checked_at` | čas kontroly |

## Výstupy

- `outputs/dashboard.html` — vizuální přehled všech služeb
- `outputs/history.csv` — historie všech měření
- `outputs/monitor.log` — log všech událostí

## Konfigurace

Weby ke sledování se nastavují v souboru `config.yaml`.
Stačí upravit seznam `weby` — každý web je jedna položka s URL.

## Automatické spouštění

Na Windows lze projekt naplánovat přes Task Scheduler.
Nastavíš čas spuštění a systém spustí `python main.py` automaticky každý den.

## Požadavky

- Python 3.12+ (nebo Docker)
- Viz `requirements.txt`