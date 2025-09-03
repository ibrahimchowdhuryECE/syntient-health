from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn

from app.routers import ask

def create_app() -> FastAPI:
    app = FastAPI(
        title="Medical Assistant Model API",
        description="Service for generating follow-up questions and patient communication",
        version="1.0.0"
    )
    
    # CORS disabled by default as specified
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[],
        allow_credentials=False,
        allow_methods=[],
        allow_headers=[],
    )
    
    # Include routers
    app.include_router(ask.router, prefix="/mam", tags=["ask"])
    
    @app.get("/health")
    async def health():
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "mam"
        }
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
