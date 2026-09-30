from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from models import User


router = APIRouter(
    prefix="/api/profile",
    tags=["Profile"]
)


# -----------------------------
# Request model
# -----------------------------

class ProfileUpdate(BaseModel):
    name: str
    email: str


# -----------------------------
# Get Profile
# -----------------------------

@router.get("/{user_id}")
def get_profile(
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

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active
    }


# -----------------------------
# Update Profile
# -----------------------------

@router.put("/{user_id}")
def update_profile(
    user_id: int,
    profile: ProfileUpdate,
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

    # Check whether email belongs to another user
    existing_user = db.query(User).filter(
        User.email == profile.email,
        User.id != user_id
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered by another user"
        )

    user.name = profile.name
    user.email = profile.email

    db.commit()
    db.refresh(user)

    return {
        "message": "Profile updated successfully",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active
        }
    }