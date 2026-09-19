from fastapi import APIRouter

from app.database import (
    check_database_connection,
    check_postgis
)

from app.redis_Client import check_redis_connection


router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("/")
def health_check():
    """
    Check the health of the backend,
    PostgreSQL/PostGIS and Redis.
    """

    database_status = check_database_connection()
    postgis_version = check_postgis()
    redis_status = check_redis_connection()

    return {
        "status": "ok",
        "backend": "running",
        "database": (
            "connected"
            if database_status
            else "disconnected"
        ),
        "postgis": (
            postgis_version
            if postgis_version
            else "unavailable"
        ),
        "redis": (
            "connected"
            if redis_status
            else "disconnected"
        )
    }