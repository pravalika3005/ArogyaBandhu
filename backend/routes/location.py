from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import get_db
from models import User, LocationUpdate
from services.location_service import (
    validate_coordinates,
    create_location_data,
    find_nearby_workers
)


router = APIRouter(
    prefix="/api/location",
    tags=["Location"]
)


# -----------------------------
# Request Models
# -----------------------------

class LocationRequest(BaseModel):
    user_id: int
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class NearbyWorkerRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    radius_km: float = Field(default=10.0, gt=0, le=100)


# -----------------------------
# Update User Location
# -----------------------------

@router.post("/update")
def update_location(
    request: LocationRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == request.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not validate_coordinates(
        request.latitude,
        request.longitude
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid latitude or longitude"
        )

    location_data = create_location_data(
        request.latitude,
        request.longitude
    )

    location = LocationUpdate(
        user_id=request.user_id,
        latitude=location_data["latitude"],
        longitude=location_data["longitude"]
    )

    db.add(location)
    db.commit()
    db.refresh(location)

    return {
        "message": "Location updated successfully",
        "location": {
            "id": location.id,
            "user_id": location.user_id,
            "latitude": location.latitude,
            "longitude": location.longitude
        }
    }


# -----------------------------
# Get Latest User Location
# -----------------------------

@router.get("/{user_id}")
def get_latest_location(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    location = (
        db.query(LocationUpdate)
        .filter(LocationUpdate.user_id == user_id)
        .order_by(LocationUpdate.created_at.desc())
        .first()
    )

    if not location:
        return {
            "message": "No location available",
            "location": None
        }

    return {
        "location": {
            "id": location.id,
            "user_id": location.user_id,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "created_at": location.created_at
        }
    }


# -----------------------------
# Location History
# -----------------------------

@router.get("/{user_id}/history")
def get_location_history(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    locations = (
        db.query(LocationUpdate)
        .filter(LocationUpdate.user_id == user_id)
        .order_by(LocationUpdate.created_at.desc())
        .all()
    )

    return {
        "user_id": user_id,
        "count": len(locations),
        "locations": [
            {
                "id": location.id,
                "latitude": location.latitude,
                "longitude": location.longitude,
                "created_at": location.created_at
            }
            for location in locations
        ]
    }


# -----------------------------
# Find Nearby ASHA Workers
# -----------------------------

@router.post("/nearby-asha")
def nearby_asha_workers(
    request: NearbyWorkerRequest,
    db: Session = Depends(get_db)
):
    if not validate_coordinates(
        request.latitude,
        request.longitude
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid latitude or longitude"
        )

    workers = find_nearby_workers(
        db=db,
        latitude=request.latitude,
        longitude=request.longitude,
        radius_km=request.radius_km
    )

    return {
        "search_location": {
            "latitude": request.latitude,
            "longitude": request.longitude
        },
        "radius_km": request.radius_km,
        "count": len(workers),
        "workers": workers
    }