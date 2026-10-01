import requests
import time
import logging
from datetime import datetime
import ssl
import socket
from urllib.parse import urlparse


def zkontroluj_ssl(url):
    try:
        hostname = urlparse(url).netloc
        ssl_valid = True
        kontext = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=10) as sock:
            with kontext.wrap_socket(sock, server_hostname=hostname) as ssock:
                certifikat = ssock.getpeercert()
                expirace_str = certifikat["notAfter"]
                expirace = datetime.strptime(expirace_str, "%b %d %H:%M:%S %Y %Z")
                zbývá_dní = expirace - datetime.now()
                ssl_expires_in_days = zbývá_dní.days
                return ssl_valid, ssl_expires_in_days
    except Exception as e:
        print(f"SSL chyba pro {hostname}: {e}")
        return False, None


def zkontroluj_web(url, cas_spusteni=None):
    try:
        hostname = urlparse(url).netloc
        zacatek = time.perf_counter()
        odpoved = requests.get(url, timeout=10)
        odpoved.raise_for_status()
        konec = time.perf_counter()
        cas_ms = (konec - zacatek) * 1000
        ssl_valid, ssl_expires_in_days = zkontroluj_ssl(url)

        return {
            "url": url,
            "is_online": True,
            "status_code": odpoved.status_code,
            "response_time_ms": cas_ms,
            "checked_at": cas_spusteni or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "page_size_kb": len(odpoved.content) / 1024,
            "ssl_valid": ssl_valid,
            "ssl_expires_in_days": ssl_expires_in_days
        }
    except Exception as e:
        logging.error(f"Chyba: {e}")
        return {
            "url": url,
            "is_online": False,
            "status_code": None,
            "response_time_ms": None,
            "checked_at": cas_spusteni or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "page_size_kb": None,
            "ssl_valid": None,
            "ssl_expires_in_days": None
        }
