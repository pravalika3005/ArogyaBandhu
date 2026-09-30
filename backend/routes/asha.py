# =========================================================
# AROGYABANDHU ASHA ROUTES
# =========================================================

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import (
    User,
    ASHAProfile,
    ASHAVisit,
    HealthRecord,
    LocationUpdate
)


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/api/asha",
    tags=["ASHA Workers"]
)


# =========================================================
# REQUEST MODELS
# =========================================================

class ASHAProfileRequest(BaseModel):

    user_id: int

    phone: str = ""

    village: str = ""

    district: str = ""

    is_available: bool = True


class LocationRequest(BaseModel):

    user_id: int

    latitude: float

    longitude: float

    accuracy: float | None = None


class ASHAVisitRequest(BaseModel):

    asha_user_id: int

    patient_user_id: int

    visit_type: str = "general"

    scheduled_at: datetime | None = None

    notes: str = ""


class VisitStatusRequest(BaseModel):

    status: str


# =========================================================
# GET ASHA PROFILE
# =========================================================

@router.get("/{user_id}")
def get_asha_profile(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="ASHA worker not found"
        )

    if user.role != "asha":

        raise HTTPException(
            status_code=400,
            detail="User is not an ASHA worker"
        )

    profile = (
        db.query(ASHAProfile)
        .filter(
            ASHAProfile.user_id == user_id
        )
        .first()
    )

    return {

        "user": {

            "id": user.id,

            "name": user.name,

            "email": user.email,

            "role": user.role
        },

        "profile": profile
    }


# =========================================================
# CREATE / UPDATE ASHA PROFILE
# =========================================================

@router.post("/profile")
def save_asha_profile(
    request: ASHAProfileRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.id == request.user_id)
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.role != "asha":

        raise HTTPException(
            status_code=400,
            detail="User is not an ASHA worker"
        )

    profile = (
        db.query(ASHAProfile)
        .filter(
            ASHAProfile.user_id == request.user_id
        )
        .first()
    )

    if profile:

        profile.phone = request.phone

        profile.village = request.village

        profile.district = request.district

        profile.is_available = (
            request.is_available
        )

    else:

        profile = ASHAProfile(

            user_id=request.user_id,

            phone=request.phone,

            village=request.village,

            district=request.district,

            is_available=
                request.is_available
        )

        db.add(profile)

    db.commit()

    db.refresh(profile)

    return {

        "message":
            "ASHA profile saved successfully",

        "profile":
            profile
    }


# =========================================================
# UPDATE ASHA LOCATION
# =========================================================

@router.post("/location")
def update_asha_location(
    request: LocationRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.id == request.user_id)
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.role != "asha":

        raise HTTPException(
            status_code=400,
            detail="User is not an ASHA worker"
        )

    if (
        request.latitude < -90
        or request.latitude > 90
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid latitude"
        )

    if (
        request.longitude < -180
        or request.longitude > 180
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid longitude"
        )

    profile = (
        db.query(ASHAProfile)
        .filter(
            ASHAProfile.user_id == request.user_id
        )
        .first()
    )

    if not profile:

        profile = ASHAProfile(
            user_id=request.user_id
        )

        db.add(profile)

    profile.latitude = request.latitude

    profile.longitude = request.longitude

    profile.last_location_update = datetime.utcnow()

    location = LocationUpdate(

        user_id=request.user_id,

        role="asha",

        latitude=request.latitude,

        longitude=request.longitude,

        accuracy=request.accuracy
    )

    db.add(location)

    db.commit()

    db.refresh(location)

    return {

        "message":
            "ASHA location updated successfully",

        "location": {

            "latitude":
                request.latitude,

            "longitude":
                request.longitude,

            "accuracy":
                request.accuracy
        }
    }


# =========================================================
# GET ASHA LOCATION
# =========================================================

@router.get("/{user_id}/location")
def get_asha_location(
    user_id: int,
    db: Session = Depends(get_db)
):

    profile = (
        db.query(ASHAProfile)
        .filter(
            ASHAProfile.user_id == user_id
        )
        .first()
    )

    if not profile:

        raise HTTPException(
            status_code=404,
            detail="ASHA profile not found"
        )

    return {

        "user_id":
            user_id,

        "latitude":
            profile.latitude,

        "longitude":
            profile.longitude,

        "last_location_update":
            profile.last_location_update
    }


# =========================================================
# CREATE ASHA VISIT
# =========================================================

@router.post("/visits")
def create_asha_visit(
    request: ASHAVisitRequest,
    db: Session = Depends(get_db)
):

    asha_user = (
        db.query(User)
        .filter(
            User.id == request.asha_user_id
        )
        .first()
    )

    if not asha_user:

        raise HTTPException(
            status_code=404,
            detail="ASHA worker not found"
        )

    if asha_user.role != "asha":

        raise HTTPException(
            status_code=400,
            detail="Selected user is not an ASHA worker"
        )

    patient = (
        db.query(User)
        .filter(
            User.id == request.patient_user_id
        )
        .first()
    )

    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    if patient.role != "patient":

        raise HTTPException(
            status_code=400,
            detail="Selected user is not a patient"
        )

    visit = ASHAVisit(

        asha_user_id=
            request.asha_user_id,

        patient_user_id=
            request.patient_user_id,

        scheduled_at=
            request.scheduled_at,

        visit_type=
            request.visit_type,

        notes=
            request.notes,

        status=
            "scheduled"
    )

    db.add(visit)

    db.commit()

    db.refresh(visit)

    return {

        "message":
            "ASHA visit scheduled successfully",

        "visit":
            visit
    }


# =========================================================
# GET ASHA VISITS
# =========================================================

@router.get("/{user_id}/visits")
def get_asha_visits(
    user_id: int,
    db: Session = Depends(get_db)
):

    visits = (
        db.query(ASHAVisit)
        .filter(
            ASHAVisit.asha_user_id == user_id
        )
        .order_by(
            ASHAVisit.scheduled_at.asc()
        )
        .all()
    )

    return {

        "asha_user_id":
            user_id,

        "visits":
            visits
    }


# =========================================================
# UPDATE VISIT STATUS
# =========================================================

@router.put("/visits/{visit_id}/status")
def update_visit_status(
    visit_id: int,
    request: VisitStatusRequest,
    db: Session = Depends(get_db)
):

    allowed_statuses = [
        "scheduled",
        "in_progress",
        "completed",
        "cancelled"
    ]

    if request.status not in allowed_statuses:

        raise HTTPException(
            status_code=400,
            detail="Invalid visit status"
        )

    visit = (
        db.query(ASHAVisit)
        .filter(
            ASHAVisit.id == visit_id
        )
        .first()
    )

    if not visit:

        raise HTTPException(
            status_code=404,
            detail="Visit not found"
        )

    visit.status = request.status

    db.commit()

    db.refresh(visit)

    return {

        "message":
            "Visit status updated successfully",

        "visit":
            visit
    }


# =========================================================
# GET ASSIGNED PATIENTS
# =========================================================

@router.get("/{user_id}/patient-directory")
def get_patient_directory(
    user_id: int,
    db: Session = Depends(get_db)
):

    asha_user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not asha_user or asha_user.role != "asha":

        raise HTTPException(
            status_code=404,
            detail="ASHA worker not found"
        )

    patients = (
        db.query(User)
        .filter(User.role == "patient")
        .order_by(User.name.asc())
        .all()
    )

    return {
        "asha_user_id": user_id,
        "patients": [
            {"id": patient.id, "name": patient.name}
            for patient in patients
        ]
    }


@router.get("/{user_id}/patients")
def get_assigned_patients(
    user_id: int,
    db: Session = Depends(get_db)
):

    visits = (
        db.query(ASHAVisit)
        .filter(
            ASHAVisit.asha_user_id == user_id
        )
        .all()
    )

    patient_ids = set()

    for visit in visits:

        patient_ids.add(
            visit.patient_user_id
        )

    patients = []

    for patient_id in patient_ids:

        patient = (
            db.query(User)
            .filter(
                User.id == patient_id
            )
            .first()
        )

        if patient:

            patients.append({

                "id":
                    patient.id,

                "name":
                    patient.name,

                "email":
                    patient.email
            })

    return {

        "asha_user_id":
            user_id,

        "patients":
            patients
    }


# =========================================================
# ADD PATIENT HEALTH RECORD
# =========================================================

class ASHAHealthRecordRequest(BaseModel):

    asha_user_id: int

    patient_user_id: int

    record_type: str

    title: str

    description: str = ""

    value: str = ""

    unit: str = ""


@router.post("/health-records")
def add_health_record(
    request: ASHAHealthRecordRequest,
    db: Session = Depends(get_db)
):

    asha = (
        db.query(User)
        .filter(
            User.id == request.asha_user_id
        )
        .first()
    )

    if not asha:

        raise HTTPException(
            status_code=404,
            detail="ASHA worker not found"
        )

    if asha.role != "asha":

        raise HTTPException(
            status_code=400,
            detail="User is not an ASHA worker"
        )

    patient = (
        db.query(User)
        .filter(
            User.id == request.patient_user_id
        )
        .first()
    )

    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    if patient.role != "patient":

        raise HTTPException(
            status_code=400,
            detail="Selected user is not a patient"
        )

    record = HealthRecord(

        patient_user_id=
            request.patient_user_id,

        record_type=
            request.record_type,

        title=
            request.title,

        description=
            request.description,

        value=
            request.value,

        unit=
            request.unit,

        recorded_by_user_id=
            request.asha_user_id
    )

    db.add(record)

    db.commit()

    db.refresh(record)

    return {

        "message":
            "Patient health record updated successfully",

        "record":
            record
    }