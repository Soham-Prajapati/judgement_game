import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import room, websocket

load_dotenv()

app = FastAPI(title="Judgement API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(room.router, prefix="/room", tags=["room"])
app.include_router(websocket.router, tags=["websocket"])


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
