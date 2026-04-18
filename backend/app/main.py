"""
Main FastAPI Application.
Entry point for the Credit Risk AI Backend.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from datetime import datetime

# Import configuration
from app.core.config import settings

# Import routes
from app.routes import health, predict, report

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Create FastAPI app instance
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered Credit Risk Scoring & Lending Decision System",
    debug=settings.DEBUG
)


# Setup CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# LIFECYCLE EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """
    Called when server starts.
    Initialize models, connect to services, etc.
    """
    logger.info("🚀 Credit Risk AI Backend Starting...")
    logger.info(f"   App: {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"   Debug: {settings.DEBUG}")
    logger.info(f"   Allowed CORS Origins: {settings.get_cors_origins()}")
    

@app.on_event("shutdown")
async def shutdown_event():
    """Called when server shuts down."""
    logger.info("🛑 Credit Risk AI Backend Shutting Down...")


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health", tags=["Health Check"])
async def health_check():
    """Simple health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================================================
# INCLUDE ROUTERS
# ============================================================================

app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(predict.router, prefix="/api", tags=["Predictions"])
app.include_router(report.router, prefix="/api", tags=["Reports"])


# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """
    Welcome message and API documentation links.
    """
    return {
        "message": "Welcome to Credit Risk AI Backend",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle any uncaught exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    # Run the app
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
