import csv
import datetime

VSTUP = "outputs/history.csv"
VYSTUP = "outputs/dashboard.html"

SVG_LOGO = """<svg width="180" height="180" viewBox="0 0 220 220" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="110" cy="110" r="100" stroke="#f5c842" stroke-width="1.5" stroke-dasharray="4 3" opacity="0.4"/>
  <circle cx="110" cy="110" r="80" stroke="#f5c842" stroke-width="0.5" opacity="0.2"/>
  <text x="110" y="21" text-anchor="middle" dominant-baseline="middle" font-size="15" fill="#f5c842">&#x271D;</text>
  <line x1="110" y1="80" x2="110" y2="28" stroke="#f5c842" stroke-width="0.4" opacity="0.25"/>
  <text x="152" y="39" text-anchor="middle" dominant-baseline="middle" font-size="15" fill="#f5c842">&#x262A;</text>
  <line x1="110" y1="80" x2="147" y2="46" stroke="#f5c842" stroke-width="0.4" opacity="0.25"/>
  <text x="185" y="68" text-anchor="middle" dominant-baseline="middle" font-size="14" fill="#f5c842">&#x0950;</text>
  <line x1="130" y1="95" x2="178" y2="72" stroke="#f5c842" stroke-width="0.4" opacity="0.25"/>
  <text x="201" y="115" text-anchor="middle" dominant-baseline="middle" font-size="14" fill="#f5c842">&#x2721;</text>
  <line x1="140" y1="110" x2="192" y2="110" stroke="#f5c842" stroke-width="0.4" opacity="0.25"/>
  <text x="185" y="157" text-anchor="middle" dominant-baseline="middle" font-size="14" fill="#f5c842">&#x2638;</text>
  <line x1="130" y1="125" x2="178" y2="150" stroke="#f5c842" stroke-width="0.4" opacity="0.25"/>
  <g transform="translate(145, 180)">
    <line x1="7" y1="-9" x2="7" y2="9" stroke="#f5c842" stroke-width="1.8"/>
    <path d="M4,-7 L2,0 L4,7" stroke="#f5c842" stroke-width="1" fill="none"/>
    <path d="M10,-7 L12,0 L10,7" stroke="#f5c842" stroke-width="1" fill="none"/>
    <circle cx="7" cy="0" r="4.5" stroke="#f5c842" stroke-width="1.2" fill="none"/>
  </g>
  <line x1="116" y1="138" x2="147" y2="175" stroke="#f5c842" stroke-width="0.4" opacity="0.25"/>
  <text x="110" y="203" text-anchor="middle" dominant-baseline="middle" font-size="14" fill="#f5c842">&#x1F35D;</text>
  <line x1="110" y1="140" x2="110" y2="196" stroke="#f5c842" stroke-width="0.4" opacity="0.25"/>
  <text x="68" y="187" text-anchor="middle" dominant-baseline="middle" font-size="14" fill="#f5c842">&#x1F3B3;</text>
  <line x1="104" y1="138" x2="72" y2="178" stroke="#f5c842" stroke-width="0.4" opacity="0.25"/>
  <text x="35" y="157" text-anchor="middle" dominant-baseline="middle" font-size="13" fill="#f5c842">&#x26E7;</text>
  <line x1="90" y1="125" x2="42" y2="150" stroke="#f5c842" stroke-width="0.4" opacity="0.25"/>
  <text x="19" y="115" text-anchor="middle" dominant-baseline="middle" font-size="11" font-weight="bold" fill="#f5c842" font-family="Georgia">JW</text>
  <line x1="80" y1="110" x2="30" y2="110" stroke="#f5c842" stroke-width="0.4" opacity="0.25"/>
  <text x="35" y="68" text-anchor="middle" dominant-baseline="middle" font-size="14" font-weight="bold" fill="#f5c842" font-family="Georgia">S</text>
  <line x1="90" y1="95" x2="42" y2="72" stroke="#f5c842" stroke-width="0.4" opacity="0.25"/>
  <circle cx="68" cy="33" r="9" stroke="#f5c842" stroke-width="1.5" fill="none" stroke-dasharray="46 8"/>
  <line x1="96" y1="82" x2="72" y2="42" stroke="#f5c842" stroke-width="0.4" opacity="0.25"/>
  <circle cx="110" cy="110" r="30" stroke="#f5c842" stroke-width="1.5" fill="#1a1225"/>
  <text x="110" y="118" text-anchor="middle" font-size="22" fill="#f5c842" font-family="Georgia">?</text>
</svg>"""


def nacti_spusteni():
    spusteni = []
    with open(VSTUP, "r", encoding="utf-8-sig") as soubor:
        reader = csv.DictReader(soubor)
        for radek in reader:
            zkraceny = radek["checked_at"][:16]  # bere jen "2026-06-02 15:07"
            if zkraceny not in spusteni:
                spusteni.append(zkraceny)
    return sorted(spusteni)


def vypocti_zmeny_pozic():
    spusteni = nacti_spusteni()
    if len(spusteni) < 2:
        return {}

    posledni_dva = spusteni[-2:]
    poradi = {}

    for cas in posledni_dva:
        weby = []
        with open(VSTUP, "r", encoding="utf-8-sig") as soubor:
            reader = csv.DictReader(soubor)
            for radek in reader:
                if radek["checked_at"][:16] == cas and radek["is_online"] == "True":
                    weby.append((radek["url"], float(radek["response_time_ms"])))
        weby.sort(key=lambda x: x[1])
        poradi[cas] = {url: i+1 for i, (url, _) in enumerate(weby)}

    zmeny = {}
    predchozi = poradi[posledni_dva[0]]
    aktualni = poradi[posledni_dva[1]]

    for url in aktualni:
        if url in predchozi:
            zmeny[url] = predchozi[url] - aktualni[url]
        else:
            zmeny[url] = 0

    return zmeny


def generuj_dashboard():
    with open(VSTUP, "r", encoding="utf-8-sig") as soubor:
        reader = csv.DictReader(soubor)
        posledni = {}
        checky = {}
        for radek in reader:
            posledni[radek["url"]] = radek
            if radek["url"] not in checky:
                checky[radek["url"]] = {"online": 0, "celkem": 0}
            checky[radek["url"]]["celkem"] += 1
            if radek["is_online"] == "True":
                checky[radek["url"]]["online"] += 1

    zmeny = vypocti_zmeny_pozic()
    online = [d for d in posledni.values() if d["is_online"] == "True"]
    offline = [d for d in posledni.values() if d["is_online"] != "True"]
    online_sorted = sorted(online, key=lambda x: float(x["response_time_ms"]) if x["response_time_ms"] else 9999)
    serazeno = online_sorted + offline

    cas = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

    with open(VYSTUP, "w", encoding="utf-8") as html:
        html.write("<!DOCTYPE html>\n")
        html.write("<html>\n")
        html.write("<head>\n")
        html.write("<meta charset='utf-8'>\n")
        html.write("<meta name='viewport' content='width=device-width, initial-scale=1'>\n")
        html.write("<style>\n")
        html.write("* { box-sizing: border-box; margin: 0; padding: 0; }\n")
        html.write("body { background: #0e0c1a; font-family: Georgia, serif; padding: 28px; color: #c0b0e0; max-width: 900px; margin: 0 auto; }\n")
        html.write(".halo-header { text-align: center; padding: 20px 0 16px; }\n")
        html.write(".title { font-size: 26px; color: #f5c842; letter-spacing: 3px; font-weight: normal; margin-top: 14px; }\n")
        html.write(".divider { border: none; border-top: 1px solid rgba(245,200,66,0.15); margin: 18px 0; }\n")
        html.write(".stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 24px; }\n")
        html.write(".stat { background: #1a1530; border: 1px solid #2a2050; border-radius: 10px; padding: 14px; text-align: center; }\n")
        html.write(".stat-n { font-size: 30px; font-weight: bold; }\n")
        html.write(".blessed { color: #4ade80; } .fallen { color: #f87171; } .watched { color: #f5c842; }\n")
        html.write(".stat-l { font-size: 10px; color: #5a4a7a; letter-spacing: 2px; margin-top: 3px; text-transform: uppercase; }\n")
        html.write("table { width: 100%; border-collapse: collapse; font-size: 13px; }\n")
        html.write("th { padding: 10px 12px; text-align: left; color: #7a6a3a; font-size: 10px; letter-spacing: 2px; border-bottom: 1px solid #2a2050; font-weight: normal; text-transform: uppercase; }\n")
        html.write("td { padding: 11px 12px; border-bottom: 1px solid #1a1530; vertical-align: middle; }\n")
        html.write(".row-b { background: #071a0e; } .row-f { background: #1a0707; }\n")
        html.write(".badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: bold; font-family: monospace; }\n")
        html.write(".bon { background: #052010; color: #4ade80; border: 1px solid #14532d; }\n")
        html.write(".bof { background: #200505; color: #f87171; border: 1px solid #7f1d1d; }\n")
        html.write(".url-cell { color: #a090c8; font-family: monospace; font-size: 12px; }\n")
        html.write(".fast { color: #4ade80; } .slow { color: #fbbf24; } .dead { color: #3a3050; }\n")
        html.write(".ssl-ok { color: #34d399; } .ssl-warn { color: #fbbf24; }\n")
        html.write(".uptime-ok { color: #4ade80; } .uptime-warn { color: #fbbf24; } .uptime-bad { color: #f87171; }\n")
        html.write(".footer { text-align: center; margin-top: 20px; font-size: 11px; color: #3a3050; letter-spacing: 1px; }\n")
        html.write("@media (max-width: 600px) { body { padding: 12px; } th, td { padding: 6px 8px; font-size: 11px; } .title { font-size: 18px; } .stat-n { font-size: 22px; } }\n")
        html.write("@keyframes pulse-up { 0%,100% { opacity:1; transform:translateY(0); } 50% { opacity:0.5; transform:translateY(-3px); } }\n")
        html.write("@keyframes pulse-down { 0%,100% { opacity:1; transform:translateY(0); } 50% { opacity:0.5; transform:translateY(3px); } }\n")
        html.write("</style>\n")
        html.write("</head>\n")
        html.write("<body>\n")
        html.write("<div class='halo-header'>\n")
        html.write(SVG_LOGO + "\n")
        html.write("<div class='title'>God Not Responding</div>\n")
        html.write("</div>\n")
        html.write("<hr class='divider'>\n")
        html.write("<div class='stats-row'>\n")
        html.write(f"<div class='stat'><div class='stat-n blessed'>{len(online)}</div><div class='stat-l'>požehnáni</div></div>\n")
        html.write(f"<div class='stat'><div class='stat-n fallen'>{len(offline)}</div><div class='stat-l'>padlí</div></div>\n")
        html.write(f"<div class='stat'><div class='stat-n watched'>{len(posledni)}</div><div class='stat-l'>pod dohledem</div></div>\n")
        html.write("</div>\n")
        html.write("<table>\n")
        html.write("<thead><tr>\n")
        html.write("<th>chrám</th><th>stav</th><th>kód</th><th>odezva (ms) &uarr;</th><th>změna pozice</th><th>SSL vyprší</th>\n")
        html.write("</tr></thead>\n")
        html.write("<tbody>\n")

        for data in serazeno:
            stav = data["is_online"] == "True"
            rychlost = round(float(data["response_time_ms"]), 2) if data["response_time_ms"] else 0
            uptime = round(checky[data["url"]]["online"] / checky[data["url"]]["celkem"] * 100)
            badge = "<span class='badge bon'>&#x2713; ONLINE</span>" if stav else "<span class='badge bof'>&#x2717; OFFLINE</span>"
            row_class = "row-b" if stav else "row-f"
            ms_class = "fast" if rychlost and rychlost < 400 else ("slow" if rychlost else "dead")
            ms_val = f"{rychlost}" if rychlost else "&#x2014;"
            dni = data["ssl_expires_in_days"] if data["ssl_expires_in_days"] else "&#x2014;"
            dni_class = "ssl-warn" if data["ssl_expires_in_days"] and int(data["ssl_expires_in_days"]) < 30 else "ssl-ok"
            html.write(f"<tr class='{row_class}'>\n")
            html.write(f"<td class='url-cell'>{data['url']}</td>\n")
            html.write(f"<td>{badge}</td>\n")
            html.write(f"<td style='color:#4a4a6a'>{data['status_code']}</td>\n")
            html.write(f"<td class='{ms_class}'>{ms_val}</td>\n")
            zmena = zmeny.get(data["url"], 0)
            if zmena > 0:
                zmena_html = f"<span style='color:#4ade80; font-size:15px; animation: pulse-up 1.5s infinite;'>▲ {zmena}</span>"
            elif zmena < 0:
                zmena_html = f"<span style='color:#f87171; font-size:15px; animation: pulse-down 1.5s infinite;'>▼ {abs(zmena)}</span>"
            else:
                zmena_html = "<span style='color:#3a3050'>&#x2014;</span>"
            html.write(f"<td>{zmena_html}</td>\n")
            html.write(f"<td class='{dni_class}'>{dni}</td>\n")
            html.write("</tr>\n")

        html.write("</tbody>\n")
        html.write("</table>\n")
        html.write(f"<div class='footer'>Poslední aktualizace: {cas}</div>\n")
        html.write("</body>\n")
        html.write("</html>\n")
