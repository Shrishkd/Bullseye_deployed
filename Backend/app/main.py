# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import auth, market, chat, health, ws_market, news
from app.services.instrument_registry import load_instruments
from app.db.session import engine
from app.models import Base


app = FastAPI(title=settings.PROJECT_NAME)

origins = ["*"]  # temporary for deploy, tighten later

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ DB ready")


app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(market.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(ws_market.router)
app.include_router(news.router, prefix="/api")


@app.get("/admin/load-instruments")
def load_all_instruments():
    load_instruments()
    return {"status": "ok"}


@app.get("/")
async def root():
    return {"message": "Bullseye backend running"}
