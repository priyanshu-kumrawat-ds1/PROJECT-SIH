from fastapi import APIRouter, HTTPException, Query

from app.services.traffic_service import (
    get_road_traffic,
    get_nearby_traffic
)


router = APIRouter(
    prefix="/traffic",
    tags=["Traffic"]
)


# --------------------------------------------------
# Get Traffic For A Road
# --------------------------------------------------

@router.get("/road/{road_id}")
def road_traffic(road_id: int):
    """
    Get traffic information for a particular road.
    """

    try:

        result = get_road_traffic(road_id)

        if result is None:

            raise HTTPException(
                status_code=404,
                detail="Road traffic data not found"
            )

        return {
            "status": "success",
            "data": result
        }

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve traffic data: {str(error)}"
        )


# --------------------------------------------------
# Get Nearby Traffic
# --------------------------------------------------

@router.get("/nearby")
def nearby_traffic(
    latitude: float = Query(
        ...,
        ge=-90,
        le=90
    ),

    longitude: float = Query(
        ...,
        ge=-180,
        le=180
    ),

    radius: int = Query(
        default=1000,
        ge=1,
        le=10000
    )
):
    """
    Get traffic information for roads
    near a geographic location.

    radius is specified in meters.
    """

    try:

        result = get_nearby_traffic(
            latitude=latitude,
            longitude=longitude,
            radius=radius
        )

        return {
            "status": "success",
            "data": result
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve nearby traffic: {str(error)}"
        )