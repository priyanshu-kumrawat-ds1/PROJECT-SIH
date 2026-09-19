from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from App.routes import health
from App.routes import routing
from App.routes import traffic


# --------------------------------------------------
# Create FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="SIH Smart Route Optimization API",
    description=(
        "Backend API for smart route optimization using "
        "PostgreSQL/PostGIS, Redis and LightGBM."
    ),
    version="1.0.0"
)


# --------------------------------------------------
# CORS Configuration
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Register API Routes
# --------------------------------------------------

app.include_router(
    health.router,
    prefix="/api"
)

app.include_router(
    routing.router,
    prefix="/api"
)

app.include_router(
    traffic.router,
    prefix="/api"
)


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "status": "success",
        "message": "SIH Smart Route Optimization Backend is running",
        "version": "1.0.0"
    }


# --------------------------------------------------
# Application Startup
# --------------------------------------------------

@app.on_event("startup")
async def startup_event():
    print("========================================")
    print(" SIH Backend Starting...")
    print("========================================")
    print("FastAPI application started")


# --------------------------------------------------
# Application Shutdown
# --------------------------------------------------

@app.on_event("shutdown")
async def shutdown_event():
    print("========================================")
    print(" SIH Backend Shutting Down...")
    print("========================================")