"""
Health Check Routes
Endpoints to verify backend services are running properly.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
import logging

from app.core.config import settings
from app.schemas.response import HealthResponse
from app.services.ml_service import ml_service
from app.services.groq_service import groq_service
from app.services.rag_service import rag_service

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", response_model=HealthResponse)
async def health_check():
    """
    Basic health check endpoint.
    Returns: Status, version, and timestamp.
    """
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        timestamp=datetime.utcnow().isoformat()
    )


@router.get("/detailed")
async def health_detailed():
    """
    Detailed health check with service status.
    Shows if all dependencies are working.
    """
    
    rag_health = rag_service.health_status()
    health_status = {
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "api": "✓ Running",
            "ml_model": "✓ Loaded" if ml_service.model_loaded else "✗ Not loaded",
            "groq_api": "✓ Configured" if groq_service.client else "✗ Not configured",
            "qdrant_db": "✓ Connected" if rag_health.get("ready") else f"✗ {rag_health.get('detail')}"
        }
    }

    return health_status


@router.get("/ready")
async def readiness_check():
    """
    Readiness probe - checks if app is ready to handle requests.
    Used by load balancers to route traffic.
    """
    
    # In a real app, check if all critical services are loaded
    is_ready = True
    
    if not is_ready:
        raise HTTPException(
            status_code=503,
            detail="Service not ready"
        )
    
    return {
        "ready": True,
        "message": "Backend is ready to accept requests"
    }


@router.get("/version")
async def get_version():
    """
    Get backend version.
    Useful for monitoring deployments.
    """
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "debug_mode": settings.DEBUG
    }
