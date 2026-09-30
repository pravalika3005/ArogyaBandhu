from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import synonym

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column("password", String, nullable=False)
    password = synonym("password_hash")
    role = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)


class PatientProfile(Base):
    __tablename__ = "patient_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey("users.id"), unique=True, nullable=False)
    phone = Column(String, default="")
    date_of_birth = Column(String, default="")
    gender = Column(String, default="")
    address = Column(Text, default="")
    village = Column(String, default="")
    district = Column(String, default="")
    blood_group = Column(String, default="")
    allergies = Column(Text, default="")
    emergency_contact = Column(String, default="")
    preferred_language = Column(String, default="english")


class DoctorProfile(Base):
    __tablename__ = "doctor_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey("users.id"), unique=True, nullable=False)
    phone = Column(String, default="")
    specialization = Column(String, default="")
    registration_number = Column(String, default="")
    hospital = Column(String, default="")
    address = Column(Text, default="")
    village = Column(String, default="")
    district = Column(String, default="")
    is_available = Column(Boolean, nullable=False, default=True)


class ASHAProfile(Base):
    __tablename__ = "asha_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey("users.id"), unique=True, nullable=False)
    phone = Column(String, default="")
    village = Column(String, default="")
    district = Column(String, default="")
    is_available = Column(Boolean, nullable=False, default=True)
    latitude = Column(Float)
    longitude = Column(Float)
    last_location_update = Column(DateTime)


class HealthRecord(Base):
    __tablename__ = "health_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_user_id = Column(ForeignKey("users.id"), nullable=False)
    record_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    value = Column(String, default="")
    unit = Column(String, default="")
    recorded_by_user_id = Column(ForeignKey("users.id"))
    recorded_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class ASHAVisit(Base):
    __tablename__ = "asha_visits"

    id = Column(Integer, primary_key=True, index=True)
    asha_user_id = Column(ForeignKey("users.id"), nullable=False)
    patient_user_id = Column(ForeignKey("users.id"), nullable=False)
    scheduled_at = Column(DateTime)
    visit_type = Column(String, default="general")
    notes = Column(Text, default="")
    status = Column(String, nullable=False, default="scheduled")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class LocationUpdate(Base):
    __tablename__ = "location_updates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    role = Column(String, default="")
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    accuracy = Column(Float)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_user_id = Column(ForeignKey("users.id"), nullable=False)
    doctor_user_id = Column(ForeignKey("users.id"), nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    consultation_type = Column(String, default="video")
    reason = Column(Text, default="")
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class ChatConversation(Base):
    __tablename__ = "chat_conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey("users.id"))
    language = Column(String, nullable=False, default="english")
    status = Column(String, nullable=False, default="active")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(
        ForeignKey("chat_conversations.id"), nullable=False
    )
    sender_type = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class PharmacyProfile(Base):
    __tablename__ = "pharmacy_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey("users.id"), unique=True, nullable=False)
    pharmacy_name = Column(String, nullable=False)
    phone = Column(String, default="")
    address = Column(Text, default="")
    village = Column(String, default="")
    district = Column(String, default="")
    latitude = Column(Float)
    longitude = Column(Float)
    is_open = Column(Boolean, nullable=False, default=True)


class MedicineInventory(Base):
    __tablename__ = "medicine_inventory"

    id = Column(Integer, primary_key=True, index=True)
    pharmacy_user_id = Column(ForeignKey("users.id"), nullable=False)
    medicine_name = Column(String, nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=0)
    unit = Column(String, nullable=False, default="units")
    requires_prescription = Column(Boolean, nullable=False, default=False)


class MedicineOrder(Base):
    __tablename__ = "medicine_orders"

    id = Column(Integer, primary_key=True, index=True)
    patient_user_id = Column(ForeignKey("users.id"), nullable=False)
    pharmacy_user_id = Column(ForeignKey("users.id"), nullable=False)
    medicine_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default="pending")
    delivery_status = Column(String, nullable=False, default="not_started")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String, nullable=False, default="general")
    is_read = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class AutomationEvent(Base):
    __tablename__ = "automation_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    event_type = Column(String, nullable=False)
    description = Column(Text, default="")
    priority = Column(String, nullable=False, default="normal")
    status = Column(String, nullable=False, default="new")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class AutomationTask(Base):
    __tablename__ = "automation_tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    event_id = Column(ForeignKey("automation_events.id"))
    patient_user_id = Column(ForeignKey("users.id"))
    assigned_to_user_id = Column(ForeignKey("users.id"))
    task_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    priority = Column(String, nullable=False, default="normal")
    status = Column(String, nullable=False, default="pending")
    due_at = Column(DateTime)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)