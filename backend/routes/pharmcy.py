# =========================================================
# AROGYABANDHU PHARMACY ROUTES
# =========================================================

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import (
    User,
    PharmacyProfile,
    MedicineInventory,
    MedicineOrder,
    Notification
)


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/api/pharmacy",
    tags=["Pharmacy"]
)


# =========================================================
# REQUEST MODELS
# =========================================================

class PharmacyProfileRequest(BaseModel):

    user_id: int

    pharmacy_name: str

    phone: str = ""

    address: str = ""

    village: str = ""

    district: str = ""

    latitude: float | None = None

    longitude: float | None = None

    is_open: bool = True


class MedicineRequest(BaseModel):

    pharmacy_user_id: int

    medicine_name: str

    quantity: int = 0

    unit: str = "units"

    requires_prescription: bool = False


class MedicineInventoryUpdateRequest(BaseModel):

    pharmacy_user_id: int

    quantity: int

    unit: str = "units"

    requires_prescription: bool = False


class MedicineOrderRequest(BaseModel):

    patient_user_id: int

    pharmacy_user_id: int

    medicine_name: str

    quantity: int = 1


# =========================================================
# SAVE PHARMACY PROFILE
# =========================================================

@router.post("/profile")
def save_pharmacy_profile(
    request: PharmacyProfileRequest,
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

    if user.role != "pharmacy":

        raise HTTPException(
            status_code=400,
            detail="User is not a pharmacy"
        )

    profile = (
        db.query(PharmacyProfile)
        .filter(
            PharmacyProfile.user_id == request.user_id
        )
        .first()
    )

    if profile:

        profile.pharmacy_name = request.pharmacy_name
        profile.phone = request.phone
        profile.address = request.address
        profile.village = request.village
        profile.district = request.district
        profile.latitude = request.latitude
        profile.longitude = request.longitude
        profile.is_open = request.is_open

    else:

        profile = PharmacyProfile(

            user_id=request.user_id,

            pharmacy_name=request.pharmacy_name,

            phone=request.phone,

            address=request.address,

            village=request.village,

            district=request.district,

            latitude=request.latitude,

            longitude=request.longitude,

            is_open=request.is_open
        )

        db.add(profile)

    db.commit()

    db.refresh(profile)

    return {

        "message":
            "Pharmacy profile saved successfully",

        "profile":
            profile
    }


# =========================================================
# GET PHARMACY PROFILE
# =========================================================

@router.get("/{user_id}")
def get_pharmacy(
    user_id: int,
    db: Session = Depends(get_db)
):

    profile = (
        db.query(PharmacyProfile)
        .filter(
            PharmacyProfile.user_id == user_id
        )
        .first()
    )

    if not profile:

        raise HTTPException(
            status_code=404,
            detail="Pharmacy profile not found"
        )

    return {

        "profile":
            profile
    }


# =========================================================
# ADD MEDICINE TO INVENTORY
# =========================================================

@router.post("/inventory")
def add_medicine(
    request: MedicineRequest,
    db: Session = Depends(get_db)
):

    pharmacy = (
        db.query(User)
        .filter(
            User.id == request.pharmacy_user_id
        )
        .first()
    )

    if not pharmacy:

        raise HTTPException(
            status_code=404,
            detail="Pharmacy user not found"
        )

    if pharmacy.role != "pharmacy":

        raise HTTPException(
            status_code=400,
            detail="Selected user is not a pharmacy"
        )

    if request.quantity < 0:

        raise HTTPException(
            status_code=400,
            detail="Quantity cannot be negative"
        )

    medicine = MedicineInventory(

        pharmacy_user_id=
            request.pharmacy_user_id,

        medicine_name=
            request.medicine_name.strip(),

        quantity=
            request.quantity,

        unit=
            request.unit,

        requires_prescription=
            request.requires_prescription
    )

    db.add(medicine)

    db.commit()

    db.refresh(medicine)

    return {

        "message":
            "Medicine added to inventory",

        "medicine":
            medicine
    }


# =========================================================
# GET PHARMACY INVENTORY
# =========================================================

@router.get("/{user_id}/inventory")
def get_inventory(
    user_id: int,
    db: Session = Depends(get_db)
):

    medicines = (
        db.query(MedicineInventory)
        .filter(
            MedicineInventory.pharmacy_user_id
            == user_id
        )
        .order_by(
            MedicineInventory.medicine_name.asc()
        )
        .all()
    )

    return {

        "pharmacy_user_id":
            user_id,

        "inventory":
            medicines
    }


# =========================================================
# SEARCH MEDICINE
# =========================================================

@router.put("/inventory/{inventory_id}")
def update_inventory_item(
    inventory_id: int,
    request: MedicineInventoryUpdateRequest,
    db: Session = Depends(get_db)
):

    pharmacy = (
        db.query(User)
        .filter(User.id == request.pharmacy_user_id)
        .first()
    )

    if not pharmacy or pharmacy.role != "pharmacy":

        raise HTTPException(
            status_code=404,
            detail="Pharmacy not found"
        )

    if request.quantity < 0:

        raise HTTPException(
            status_code=400,
            detail="Quantity cannot be negative"
        )

    medicine = (
        db.query(MedicineInventory)
        .filter(
            MedicineInventory.id == inventory_id,
            MedicineInventory.pharmacy_user_id == pharmacy.id
        )
        .first()
    )

    if not medicine:

        raise HTTPException(
            status_code=404,
            detail="Inventory item not found"
        )

    medicine.quantity = request.quantity
    medicine.unit = request.unit.strip() or "units"
    medicine.requires_prescription = request.requires_prescription

    db.commit()
    db.refresh(medicine)

    return {
        "message": "Inventory updated successfully",
        "medicine": medicine
    }

@router.get("/search/{medicine_name}")
def search_medicine(
    medicine_name: str,
    db: Session = Depends(get_db)
):

    search_text = (
        medicine_name.strip().lower()
    )

    medicines = (
        db.query(MedicineInventory)
        .filter(
            MedicineInventory.medicine_name
            .ilike(f"%{search_text}%")
        )
        .all()
    )

    results = []

    for medicine in medicines:

        pharmacy = (
            db.query(PharmacyProfile)
            .filter(
                PharmacyProfile.user_id
                == medicine.pharmacy_user_id
            )
            .first()
        )

        results.append({

            "medicine":
                medicine,

            "pharmacy":
                pharmacy
        })

    return {

        "medicine_name":
            medicine_name,

        "results":
            results
    }


# =========================================================
# CREATE MEDICINE ORDER
# =========================================================

@router.post("/orders")
def create_medicine_order(
    request: MedicineOrderRequest,
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

    pharmacy = (
        db.query(User)
        .filter(
            User.id == request.pharmacy_user_id
        )
        .first()
    )

    if not pharmacy:

        raise HTTPException(
            status_code=404,
            detail="Pharmacy not found"
        )

    if pharmacy.role != "pharmacy":

        raise HTTPException(
            status_code=400,
            detail="Selected user is not a pharmacy"
        )

    if request.quantity <= 0:

        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero"
        )

    medicine = (
        db.query(MedicineInventory)
        .filter(
            MedicineInventory.pharmacy_user_id
            == request.pharmacy_user_id
        )
        .filter(
            MedicineInventory.medicine_name
            .ilike(request.medicine_name.strip())
        )
        .first()
    )

    if not medicine:

        raise HTTPException(
            status_code=404,
            detail="Medicine not available in this pharmacy"
        )

    if medicine.quantity < request.quantity:

        raise HTTPException(
            status_code=400,
            detail="Insufficient medicine stock"
        )

    order = MedicineOrder(

        patient_user_id=
            request.patient_user_id,

        pharmacy_user_id=
            request.pharmacy_user_id,

        medicine_name=
            request.medicine_name.strip(),

        quantity=
            request.quantity,

        status=
            "pending",

        delivery_status=
            "not_started"
    )

    medicine.quantity -= request.quantity

    db.add(order)

    db.commit()

    db.refresh(order)

    return {

        "message":
            "Medicine order created successfully",

        "order":
            order
    }


# =========================================================
# GET MEDICINE ORDERS FOR PATIENT
# =========================================================

@router.get("/orders/patient/{patient_user_id}")
def get_patient_orders(
    patient_user_id: int,
    db: Session = Depends(get_db)
):

    orders = (
        db.query(MedicineOrder)
        .filter(
            MedicineOrder.patient_user_id
            == patient_user_id
        )
        .order_by(
            MedicineOrder.created_at.desc()
        )
        .all()
    )

    return {

        "patient_user_id":
            patient_user_id,

        "orders":
            orders
    }


# =========================================================
# GET MEDICINE ORDERS FOR PHARMACY
# =========================================================

@router.get("/orders/pharmacy/{pharmacy_user_id}")
def get_pharmacy_orders(
    pharmacy_user_id: int,
    db: Session = Depends(get_db)
):

    orders = (
        db.query(MedicineOrder)
        .filter(
            MedicineOrder.pharmacy_user_id
            == pharmacy_user_id
        )
        .order_by(
            MedicineOrder.created_at.desc()
        )
        .all()
    )

    order_results = []

    for order in orders:
        patient = (
            db.query(User)
            .filter(User.id == order.patient_user_id)
            .first()
        )
        order_results.append({
            "order": order,
            "patient": {
                "id": patient.id if patient else None,
                "name": patient.name if patient else "Patient"
            }
        })

    return {

        "pharmacy_user_id":
            pharmacy_user_id,

        "orders":
            order_results
    }


# =========================================================
# UPDATE ORDER STATUS
# =========================================================

class OrderStatusRequest(BaseModel):

    status: str

    delivery_status: str = "not_started"

    pharmacy_user_id: int


@router.put("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    request: OrderStatusRequest,
    db: Session = Depends(get_db)
):

    allowed_statuses = [
        "pending",
        "accepted",
        "rejected",
        "processing",
        "completed",
        "cancelled"
    ]

    allowed_delivery_statuses = [
        "not_started",
        "preparing",
        "out_for_delivery",
        "delivered"
    ]

    if request.status not in allowed_statuses:

        raise HTTPException(
            status_code=400,
            detail="Invalid order status"
        )

    if (
        request.delivery_status
        not in allowed_delivery_statuses
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid delivery status"
        )

    order = (
        db.query(MedicineOrder)
        .filter(
            MedicineOrder.id == order_id
        )
        .first()
    )

    if not order:

        raise HTTPException(
            status_code=404,
            detail="Medicine order not found"
        )

    if order.pharmacy_user_id != request.pharmacy_user_id:

        raise HTTPException(
            status_code=403,
            detail="This order belongs to another pharmacy"
        )

    previous_status = order.status
    previous_delivery_status = order.delivery_status

    order.status = request.status

    order.delivery_status = (
        request.delivery_status
    )

    if (
        order.status != previous_status
        or order.delivery_status != previous_delivery_status
    ):
        delivery_text = (
            f" Delivery status: {request.delivery_status.replace('_', ' ')}."
            if request.delivery_status != "not_started"
            else ""
        )
        notification = Notification(
            user_id=order.patient_user_id,
            title="Medicine request update",
            message=(
                f"Your request for {order.medicine_name} is now "
                f"{request.status.replace('_', ' ')}.{delivery_text}"
            ),
            notification_type="medicine"
        )
        db.add(notification)

    db.commit()

    db.refresh(order)

    return {

        "message":
            "Medicine order updated successfully",

        "order":
            order
    }