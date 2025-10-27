from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

from app.config import setup_logging
from app.api.routes import characters, health

# Setup logging
logger = setup_logging()

# Initialize FastAPI application
app = FastAPI(
    title="Character API",
    description="API for managing character data",
    version="1.0.0"
)

# Setup Prometheus instrumentation
Instrumentator().instrument(app).expose(app)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    """Request validation error handler."""
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors()},
    )


# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(characters.router, tags=["characters"])
