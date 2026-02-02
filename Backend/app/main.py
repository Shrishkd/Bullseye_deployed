from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import auth, market, chat, health, ws_market, news
from app.services.instrument_registry import load_instruments
from app.db.session import engine
from app.models import Base

app = FastAPI()

@app.get("/")
def root():
    return {"ok": True}
