# =========================================================
# AROGYABANDHU DOCTOR ROUTES
# =========================================================

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import (
    User,
    DoctorProfile,
    HealthRecord,
    Appointment,
    Notification
)


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/api/doctors",
    tags=["Doctors"]
)


# =========================================================
# REQUEST MODELS
# =========================================================

class DoctorProfileRequest(BaseModel):

    user_id: int

    phone: str = ""

    specialization: str = ""

    registration_number: str = ""

    hospital: str = ""

    address: str = ""

    village: str = ""

    district: str = ""

    is_available: bool = True


class DoctorAvailabilityRequest(BaseModel):

    user_id: int

    is_available: bool


class DoctorFollowUpRequest(BaseModel):

    doctor_user_id: int

    patient_user_id: int

    message: str


class DoctorMedicationNoteRequest(BaseModel):

    doctor_user_id: int

    patient_user_id: int

    medicine_name: str

    instructions: str


# =========================================================
# GET DOCTOR
# =========================================================

@router.get("/{user_id}")
def get_doctor(
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
            detail="Doctor not found"
        )

    if user.role != "doctor":

        raise HTTPException(
            status_code=400,
            detail="User is not a doctor"
        )

    profile = (
        db.query(DoctorProfile)
        .filter(
            DoctorProfile.user_id == user_id
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
# CREATE / UPDATE DOCTOR PROFILE
# =========================================================

@router.post("/profile")
def save_doctor_profile(
    request: DoctorProfileRequest,
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

    if user.role != "doctor":

        raise HTTPException(
            status_code=400,
            detail="User is not a doctor"
        )

    profile = (
        db.query(DoctorProfile)
        .filter(
            DoctorProfile.user_id == request.user_id
        )
        .first()
    )

    if profile:

        profile.phone = request.phone

        profile.specialization = (
            request.specialization
        )

        profile.registration_number = (
            request.registration_number
        )

        profile.hospital = request.hospital

        profile.address = request.address

        profile.village = request.village

        profile.district = request.district

        profile.is_available = (
            request.is_available
        )

    else:

        profile = DoctorProfile(

            user_id=request.user_id,

            phone=request.phone,

            specialization=
                request.specialization,

            registration_number=
                request.registration_number,

            hospital=request.hospital,

            address=request.address,

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
            "Doctor profile saved successfully",

        "profile":
            profile
    }


# =========================================================
# UPDATE DOCTOR AVAILABILITY
# =========================================================

@router.put("/availability")
def update_doctor_availability(
    request: DoctorAvailabilityRequest,
    db: Session = Depends(get_db)
):

    profile = (
        db.query(DoctorProfile)
        .filter(
            DoctorProfile.user_id == request.user_id
        )
        .first()
    )

    if not profile:

        raise HTTPException(
            status_code=404,
            detail="Doctor profile not found"
        )

    profile.is_available = (
        request.is_available
    )

    db.commit()

    db.refresh(profile)

    return {

        "message":
            "Doctor availability updated",

        "is_available":
            profile.is_available
    }


# =========================================================
# GET AVAILABLE DOCTORS
# =========================================================

@router.get("/")
def get_available_doctors(
    db: Session = Depends(get_db)
):

    doctors = (
        db.query(DoctorProfile)
        .filter(
            DoctorProfile.is_available == True
        )
        .all()
    )

    result = []

    for doctor in doctors:

        user = (
            db.query(User)
            .filter(
                User.id == doctor.user_id
            )
            .first()
        )

        if user:

            result.append({

                "user_id":
                    user.id,

                "name":
                    user.name,

                "email":
                    user.email,

                "specialization":
                    doctor.specialization,

                "hospital":
                    doctor.hospital,

                "village":
                    doctor.village,

                "district":
                    doctor.district,

                "is_available":
                    doctor.is_available
            })

    return {

        "doctors":
            result
    }


# =========================================================
# SEND PATIENT FOLLOW-UP MESSAGE
# =========================================================

@router.post("/follow-up")
def send_patient_follow_up(
    request: DoctorFollowUpRequest,
    db: Session = Depends(get_db)
):

    doctor = (
        db.query(User)
        .filter(User.id == request.doctor_user_id)
        .first()
    )

    if not doctor or doctor.role != "doctor":

        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    patient = (
        db.query(User)
        .filter(User.id == request.patient_user_id)
        .first()
    )

    if not patient or patient.role != "patient":

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    message = request.message.strip()

    if not message:

        raise HTTPException(
            status_code=400,
            detail="Follow-up message cannot be empty"
        )

    if len(message) > 1000:

        raise HTTPException(
            status_code=400,
            detail="Follow-up message must be 1000 characters or fewer"
        )

    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_user_id == doctor.id,
            Appointment.patient_user_id == patient.id,
            Appointment.status.in_(["confirmed", "completed"])
        )
        .first()
    )

    if not appointment:

        raise HTTPException(
            status_code=403,
            detail="A confirmed or completed appointment is required"
        )

    notification = Notification(
        user_id=patient.id,
        title="Doctor follow-up",
        message=message,
        notification_type="doctor_followup"
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return {
        "message": "Follow-up message sent",
        "notification": {
            "id": notification.id,
            "user_id": notification.user_id,
            "title": notification.title,
            "message": notification.message,
            "notification_type": notification.notification_type,
            "created_at": notification.created_at
        }
    }


# =========================================================
# SAVE DOCTOR MEDICATION NOTE
# =========================================================

@router.post("/medication-note")
def save_medication_note(
    request: DoctorMedicationNoteRequest,
    db: Session = Depends(get_db)
):

    doctor = (
        db.query(User)
        .filter(User.id == request.doctor_user_id)
        .first()
    )

    if not doctor or doctor.role != "doctor":

        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    patient = (
        db.query(User)
        .filter(User.id == request.patient_user_id)
        .first()
    )

    if not patient or patient.role != "patient":

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    medicine_name = request.medicine_name.strip()
    instructions = request.instructions.strip()

    if not medicine_name or len(medicine_name) > 120:

        raise HTTPException(
            status_code=400,
            detail="Medicine name is required and must be 120 characters or fewer"
        )

    if not instructions or len(instructions) > 1000:

        raise HTTPException(
            status_code=400,
            detail="Instructions are required and must be 1000 characters or fewer"
        )

    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_user_id == doctor.id,
            Appointment.patient_user_id == patient.id,
            Appointment.status.in_(["confirmed", "completed"])
        )
        .first()
    )

    if not appointment:

        raise HTTPException(
            status_code=403,
            detail="A confirmed or completed visit is required"
        )

    record = HealthRecord(
        patient_user_id=patient.id,
        record_type="Medication",
        title=f"Medication note: {medicine_name}",
        description=instructions,
        recorded_by_user_id=doctor.id
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "message": "Medication note saved to patient health records",
        "record": {
            "id": record.id,
            "patient_user_id": record.patient_user_id,
            "record_type": record.record_type,
            "title": record.title,
            "description": record.description,
            "recorded_by_user_id": record.recorded_by_user_id,
            "recorded_at": record.recorded_at
        }
    }


# =========================================================
# VIEW PATIENT HEALTH RECORDS
# =========================================================

@router.get("/patient/{patient_user_id}/records")
def get_patient_records(
    patient_user_id: int,
    doctor_user_id: int,
    db: Session = Depends(get_db)
):

    patient = (
        db.query(User)
        .filter(
            User.id == patient_user_id
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

    doctor = (
        db.query(User)
        .filter(User.id == doctor_user_id)
        .first()
    )

    if not doctor or doctor.role != "doctor":

        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_user_id == doctor.id,
            Appointment.patient_user_id == patient.id,
            Appointment.status.in_(["confirmed", "completed"])
        )
        .first()
    )

    if not appointment:

        raise HTTPException(
            status_code=403,
            detail="A confirmed or completed visit is required"
        )

    records = (
        db.query(HealthRecord)
        .filter(
            HealthRecord.patient_user_id
            == patient_user_id
        )
        .order_by(
            HealthRecord.recorded_at.desc()
        )
        .all()
    )

    return {

        "patient": {

            "id":
                patient.id,

            "name":
                patient.name,

            "email":
                patient.email
        },

        "records":
            records
    }