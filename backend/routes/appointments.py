# =========================================================
# AROGYABANDHU APPOINTMENT ROUTES
# =========================================================

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import (
    User,
    Appointment
)


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/api/appointments",
    tags=["Appointments"]
)


# =========================================================
# REQUEST MODELS
# =========================================================

class AppointmentRequest(BaseModel):

    patient_user_id: int

    doctor_user_id: int

    appointment_date: datetime

    consultation_type: str = "video"

    reason: str = ""


class AppointmentStatusRequest(BaseModel):

    status: str


# =========================================================
# CREATE APPOINTMENT
# =========================================================

@router.post("/")
def create_appointment(
    request: AppointmentRequest,
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


    doctor = (
        db.query(User)
        .filter(
            User.id == request.doctor_user_id
        )
        .first()
    )

    if not doctor:

        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    if doctor.role != "doctor":

        raise HTTPException(
            status_code=400,
            detail="Selected user is not a doctor"
        )


    allowed_types = [
        "video",
        "chat",
        "in_person"
    ]

    if request.consultation_type not in allowed_types:

        raise HTTPException(
            status_code=400,
            detail="Invalid consultation type"
        )


    if request.appointment_date <= datetime.now():

        raise HTTPException(
            status_code=400,
            detail="Appointment date must be in the future"
        )


    appointment = Appointment(

        patient_user_id=
            request.patient_user_id,

        doctor_user_id=
            request.doctor_user_id,

        appointment_date=
            request.appointment_date,

        consultation_type=
            request.consultation_type,

        reason=
            request.reason,

        status=
            "pending"
    )


    db.add(appointment)

    db.commit()

    db.refresh(appointment)


    return {

        "message":
            "Appointment created successfully",

        "appointment":
            appointment
    }


# =========================================================
# GET PATIENT APPOINTMENTS
# =========================================================

@router.get("/patient/{patient_user_id}")
def get_patient_appointments(
    patient_user_id: int,
    db: Session = Depends(get_db)
):

    appointments = (
        db.query(Appointment)
        .filter(
            Appointment.patient_user_id
            == patient_user_id
        )
        .order_by(
            Appointment.appointment_date.asc()
        )
        .all()
    )


    results = []


    for appointment in appointments:

        doctor = (
            db.query(User)
            .filter(
                User.id
                == appointment.doctor_user_id
            )
            .first()
        )


        results.append({

            "appointment":
                appointment,

            "doctor": {

                "id":
                    doctor.id
                    if doctor else None,

                "name":
                    doctor.name
                    if doctor else "Unknown"
            }
        })


    return {

        "patient_user_id":
            patient_user_id,

        "appointments":
            results
    }


# =========================================================
# GET DOCTOR APPOINTMENTS
# =========================================================

@router.get("/doctor/{doctor_user_id}")
def get_doctor_appointments(
    doctor_user_id: int,
    db: Session = Depends(get_db)
):

    appointments = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_user_id
            == doctor_user_id
        )
        .order_by(
            Appointment.appointment_date.asc()
        )
        .all()
    )


    results = []


    for appointment in appointments:

        patient = (
            db.query(User)
            .filter(
                User.id
                == appointment.patient_user_id
            )
            .first()
        )


        results.append({

            "appointment":
                appointment,

            "patient": {

                "id":
                    patient.id
                    if patient else None,

                "name":
                    patient.name
                    if patient else "Unknown"
            }
        })


    return {

        "doctor_user_id":
            doctor_user_id,

        "appointments":
            results
    }


# =========================================================
# GET SINGLE APPOINTMENT
# =========================================================

@router.get("/{appointment_id}")
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):

    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.id == appointment_id
        )
        .first()
    )


    if not appointment:

        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )


    return {

        "appointment":
            appointment
    }


# =========================================================
# UPDATE APPOINTMENT STATUS
# =========================================================

@router.put("/{appointment_id}/status")
def update_appointment_status(
    appointment_id: int,
    request: AppointmentStatusRequest,
    db: Session = Depends(get_db)
):

    allowed_statuses = [

        "pending",

        "confirmed",

        "completed",

        "cancelled",

        "rejected",

        "no_show"
    ]


    if request.status not in allowed_statuses:

        raise HTTPException(
            status_code=400,
            detail="Invalid appointment status"
        )


    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.id == appointment_id
        )
        .first()
    )


    if not appointment:

        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )


    appointment.status = request.status


    db.commit()

    db.refresh(appointment)


    return {

        "message":
            "Appointment status updated successfully",

        "appointment":
            appointment
    }


# =========================================================
# CANCEL APPOINTMENT
# =========================================================

@router.delete("/{appointment_id}")
def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):

    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.id == appointment_id
        )
        .first()
    )


    if not appointment:

        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )


    appointment.status = "cancelled"


    db.commit()

    db.refresh(appointment)


    return {

        "message":
            "Appointment cancelled successfully",

        "appointment":
            appointment
    }