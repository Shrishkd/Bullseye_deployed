# app/api/v1/ws_market.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.market_providers.router import get_provider
import asyncio

router = APIRouter()


@router.websocket("/ws/market/{symbol}")
async def market_ws(websocket: WebSocket, symbol: str):
    await websocket.accept()

    try:
        provider, instrument_key = await get_provider(symbol)

        while True:
            quote = await provider.fetch_quote(instrument_key)

            if quote:
                await websocket.send_json({
                    "symbol": symbol.upper(),
                    "price": quote.get("price"),
                })

            # ✅ Important for Render memory stability
            await asyncio.sleep(2)

    except WebSocketDisconnect:
        pass

    except Exception as e:
        try:
            await websocket.send_json({"error": str(e)})
        finally:
            await websocket.close()
