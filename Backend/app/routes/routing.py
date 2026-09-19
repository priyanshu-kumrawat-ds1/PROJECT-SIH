from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.routing_service import optimize_route


router = APIRouter(
    prefix="/routing",
    tags=["Routing"]
)


# --------------------------------------------------
# Request Models
# --------------------------------------------------

class Location(BaseModel):
    latitude: float = Field(
        ...,
        ge=-90,
        le=90
    )

    longitude: float = Field(
        ...,
        ge=-180,
        le=180
    )


class RoutingRequest(BaseModel):
    source: Location

    destination: Location

    vehicle_type: str = Field(
        default="car"
    )

    departure_time: Optional[datetime] = None


# --------------------------------------------------
# Route Optimization Endpoint
# --------------------------------------------------

@router.post("/optimize")
def optimize_routing(request: RoutingRequest):
    """
    Request optimized routes between source
    and destination.

    The actual routing, ML prediction and
    QPSO optimization are handled by the
    service/optimization layers.
    """

    try:

        result = optimize_route(
            source=request.source.model_dump(),
            destination=request.destination.model_dump(),
            vehicle_type=request.vehicle_type,
            departure_time=request.departure_time
        )

        return {
            "status": "success",
            "data": result
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Route optimization failed: {str(error)}"
        )