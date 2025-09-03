from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn

from app.routers import propose

def create_app() -> FastAPI:
    app = FastAPI(
        title="Clash/Booking Model API",
        description="Appointment scheduling and optimization service with OR-Tools integration",
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
    app.include_router(propose.router, prefix="/cmm", tags=["propose"])
    
    @app.get("/health")
    async def health():
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "cmm"
        }
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
