from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn

from app.routers import evaluate

def create_app() -> FastAPI:
    app = FastAPI(
        title="Diagnosis Model API",
        description="Triage and urgency evaluation service for medical complaints",
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
    app.include_router(evaluate.router, prefix="/dm", tags=["evaluate"])
    
    @app.get("/health")
    async def health():
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "dm"
        }
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
