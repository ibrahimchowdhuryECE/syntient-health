from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn

from app.routers import search

def create_app() -> FastAPI:
    app = FastAPI(
        title="Retrieval Service API",
        description="RAG (Retrieval-Augmented Generation) service for medical knowledge base search",
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
    app.include_router(search.router, prefix="/kb", tags=["search"])
    
    @app.get("/health")
    async def health():
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "retrieval"
        }
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
