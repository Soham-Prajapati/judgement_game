from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
from dotenv import load_dotenv
from routers import room, websocket

load_dotenv()

app = FastAPI(title="Project Judgement (Kachuful)")

# 1. PERMISSIVE CORS (Crucial for APKs to talk to Railway)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. PRIORITY ROUTERS (API and WS must be registered BEFORE static catch-all)
app.include_router(room.router)
app.include_router(websocket.router)

# 3. STATIC WEB APP (Optional, for playing in browser)
if os.path.exists("static"):
    # Mount static files under /browser so they don't conflict with /ws
    app.mount("/browser", StaticFiles(directory="static"), name="static")

    @app.get("/")
    async def serve_home():
        return FileResponse("static/index.html")

    @app.get("/play/{full_path:path}")
    async def serve_frontend(full_path: str):
        return FileResponse("static/index.html")
else:
    @app.get("/")
    async def health():
        return {"status": "Judgement Backend Live"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
