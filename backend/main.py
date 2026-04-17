from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
from dotenv import load_dotenv
from routers import room, websocket
import os

load_dotenv()

app = FastAPI(title="Project Judgement (Kachuful)")

# Configure CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(room.router)
app.include_router(websocket.router)

# Serve the Frontend Web App
# We will put the built files in a folder called 'static'
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Serve the index.html for any route to support SPA navigation
        return FileResponse("static/index.html")
else:
    @app.get("/")
    async def health_check():
        return {"status": "Backend Live - Static folder not found yet"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
