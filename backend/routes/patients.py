# =========================================================
# AROGYABANDHU PATIENT ROUTES
# =========================================================

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import (
    User,
    PatientProfile,
    HealthRecord
)


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/api/patients",
    tags=["Patients"]
)


# =========================================================
# REQUEST MODELS
# =========================================================

class PatientProfileRequest(BaseModel):

    user_id: int

    phone: str = ""

    date_of_birth: str = ""

    gender: str = ""

    address: str = ""

    village: str = ""

    district: str = ""

    blood_group: str = ""

    allergies: str = ""

    emergency_contact: str = ""

    preferred_language: str = "english"


class HealthRecordRequest(BaseModel):

    patient_user_id: int

    record_type: str

    title: str

    description: str = ""

    value: str = ""

    unit: str = ""

    recorded_by_user_id: int | None = None


# =========================================================
# GET PATIENT
# =========================================================

@router.get("/{user_id}")
def get_patient(
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
            detail="Patient not found"
        )

    if user.role != "patient":

        raise HTTPException(
            status_code=400,
            detail="User is not a patient"
        )

    profile = (
        db.query(PatientProfile)
        .filter(
            PatientProfile.user_id == user_id
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
# CREATE / UPDATE PATIENT PROFILE
# =========================================================

@router.post("/profile")
def save_patient_profile(
    request: PatientProfileRequest,
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

    if user.role != "patient":

        raise HTTPException(
            status_code=400,
            detail="User is not a patient"
        )

    profile = (
        db.query(PatientProfile)
        .filter(
            PatientProfile.user_id == request.user_id
        )
        .first()
    )

    if profile:

        profile.phone = request.phone
        profile.date_of_birth = request.date_of_birth
        profile.gender = request.gender
        profile.address = request.address
        profile.village = request.village
        profile.district = request.district
        profile.blood_group = request.blood_group
        profile.allergies = request.allergies
        profile.emergency_contact = request.emergency_contact
        profile.preferred_language = request.preferred_language

    else:

        profile = PatientProfile(

            user_id=request.user_id,

            phone=request.phone,

            date_of_birth=request.date_of_birth,

            gender=request.gender,

            address=request.address,

            village=request.village,

            district=request.district,

            blood_group=request.blood_group,

            allergies=request.allergies,

            emergency_contact=request.emergency_contact,

            preferred_language=request.preferred_language
        )

        db.add(profile)

    db.commit()

    db.refresh(profile)

    return {

        "message":
            "Patient profile saved successfully",

        "profile":
            profile
    }


# =========================================================
# ADD HEALTH RECORD
# =========================================================

@router.post("/records")
def add_health_record(
    request: HealthRecordRequest,
    db: Session = Depends(get_db)
):

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
            request.recorded_by_user_id
    )

    db.add(record)

    db.commit()

    db.refresh(record)

    return {

        "message":
            "Health record added successfully",

        "record":
            record
    }


# =========================================================
# GET HEALTH RECORDS
# =========================================================

@router.get("/{user_id}/records")
def get_health_records(
    user_id: int,
    db: Session = Depends(get_db)
):

    patient = (
        db.query(User)
        .filter(User.id == user_id)
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
            detail="User is not a patient"
        )

    records = (
        db.query(HealthRecord)
        .filter(
            HealthRecord.patient_user_id == user_id
        )
        .order_by(
            HealthRecord.recorded_at.desc()
        )
        .all()
    )

    return {

        "patient_user_id":
            user_id,

        "records":
            records
    }
