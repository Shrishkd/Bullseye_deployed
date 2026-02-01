# app/services/instrument_registry.py

import os
import csv
import gzip
import requests
import io
from datetime import datetime, timedelta

INSTRUMENT_URL = "https://assets.upstox.com/market-quote/instruments/exchange/NSE.csv.gz"
CACHE_DIR = "data"
CACHE_FILE = os.path.join(CACHE_DIR, "nse_instruments.csv")
CACHE_TTL_HOURS = 24

_symbol_map = {}
_loaded = False


def _cache_valid():
    if not os.path.exists(CACHE_FILE):
        return False
    mtime = datetime.fromtimestamp(os.path.getmtime(CACHE_FILE))
    return datetime.now() - mtime < timedelta(hours=CACHE_TTL_HOURS)


def _get_symbol(row: dict) -> str | None:
    return row.get("tradingsymbol") or row.get("symbol")


def _load():
    global _loaded, _symbol_map

    if _loaded:
        return

    os.makedirs(CACHE_DIR, exist_ok=True)

    if not _cache_valid():
        r = requests.get(INSTRUMENT_URL, timeout=30)
        r.raise_for_status()

        with gzip.open(io.BytesIO(r.content), "rt", encoding="utf-8") as gz:
            reader = csv.DictReader(gz)
            with open(CACHE_FILE, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, reader.fieldnames)
                writer.writeheader()

                for row in reader:
                    if row.get("exchange") == "NSE_EQ":
                        writer.writerow(row)

    with open(CACHE_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            symbol = _get_symbol(row)
            instrument_key = row.get("instrument_key")
            if symbol and instrument_key:
                _symbol_map[symbol.upper()] = instrument_key

    _loaded = True
    print(f"Loaded {_symbol_map.__len__()} NSE instruments")


def resolve_symbol(symbol: str):
    if not _loaded:
        _load()
    return _symbol_map.get(symbol.upper())
