# app/services/market_providers/router.py

from app.services.instrument_registry import resolve_symbol
from app.services.market_providers.upstox import UpstoxProvider


async def get_provider(symbol: str):
    instrument_key = resolve_symbol(symbol)
    provider = UpstoxProvider()
    return provider, instrument_key
