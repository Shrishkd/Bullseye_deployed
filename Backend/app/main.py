from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.services.instrument_registry import load_instruments

app = FastAPI()

@app.get("/")
def root():
    return {"ok": True}
