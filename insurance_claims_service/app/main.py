"""FastAPI application entry point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime

from app.config import settings
from app.routers import (
    auth_router,
    policy_router,
    claim_router,
    customer_router,
    agent_router,
    insurer_router,
    premium_router,
    coverage_router,
    beneficiary_router,
    underwriter_router,
    risk_assessment_router,
    payment_router,
    document_router,
    incident_router,
    vehicle_router,
    property_router,
    medical_record_router,
    quote_router,
    policy_renewal_router,
    commission_router,
    endorsement_router,
)

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="High-performance insurance claims management API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/v1/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=[settings.CORS_ALLOW_METHODS],
    allow_headers=[settings.CORS_ALLOW_HEADERS],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/api/v1/system/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        content={
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": settings.APP_VERSION,
        }
    )


@app.get("/api/v1/system/ready")
async def readiness_check():
    """Readiness check endpoint"""
    # TODO: Add database and Redis connectivity checks
    return JSONResponse(
        content={
            "status": "ready",
            "timestamp": datetime.utcnow().isoformat(),
        }
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Debug mode: {settings.DEBUG}")
    print(f"Swagger UI: http://{settings.HOST}:{settings.PORT}/docs")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    print(f"Shutting down {settings.APP_NAME}")


# Include authentication router
app.include_router(auth_router, prefix="/api/v1")

# Include entity routers
app.include_router(policy_router, prefix="/api/v1")
app.include_router(claim_router, prefix="/api/v1")
app.include_router(customer_router, prefix="/api/v1")
app.include_router(agent_router, prefix="/api/v1")
app.include_router(insurer_router, prefix="/api/v1")
app.include_router(premium_router, prefix="/api/v1")
app.include_router(coverage_router, prefix="/api/v1")
app.include_router(beneficiary_router, prefix="/api/v1")
app.include_router(underwriter_router, prefix="/api/v1")
app.include_router(risk_assessment_router, prefix="/api/v1")
app.include_router(payment_router, prefix="/api/v1")
app.include_router(document_router, prefix="/api/v1")
app.include_router(incident_router, prefix="/api/v1")
app.include_router(vehicle_router, prefix="/api/v1")
app.include_router(property_router, prefix="/api/v1")
app.include_router(medical_record_router, prefix="/api/v1")
app.include_router(quote_router, prefix="/api/v1")
app.include_router(policy_renewal_router, prefix="/api/v1")
app.include_router(commission_router, prefix="/api/v1")
app.include_router(endorsement_router, prefix="/api/v1")
