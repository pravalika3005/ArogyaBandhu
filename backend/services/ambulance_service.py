# =========================================================
# AROGYABANDHU AMBULANCE SERVICE
# =========================================================

from math import radians, sin, cos, sqrt, atan2


# =========================================================
# DISTANCE CALCULATION
# =========================================================

def calculate_distance(
    latitude1: float,
    longitude1: float,
    latitude2: float,
    longitude2: float
) -> float:

    earth_radius = 6371.0

    lat1 = radians(latitude1)
    lon1 = radians(longitude1)

    lat2 = radians(latitude2)
    lon2 = radians(longitude2)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (
        sin(delta_lat / 2) ** 2
        +
        cos(lat1)
        * cos(lat2)
        * sin(delta_lon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return round(
        earth_radius * c,
        2
    )


# =========================================================
# VALIDATE LOCATION
# =========================================================

def validate_location(
    latitude: float,
    longitude: float
) -> bool:

    if latitude < -90 or latitude > 90:
        return False

    if longitude < -180 or longitude > 180:
        return False

    return True


# =========================================================
# FIND NEAREST AVAILABLE AMBULANCE
# =========================================================

def find_nearest_ambulance(
    ambulances: list,
    patient_latitude: float,
    patient_longitude: float
):

    nearest_ambulance = None
    shortest_distance = None

    for ambulance in ambulances:

        if ambulance.get("status") != "available":
            continue

        latitude = ambulance.get("latitude")
        longitude = ambulance.get("longitude")

        if latitude is None or longitude is None:
            continue

        distance = calculate_distance(
            patient_latitude,
            patient_longitude,
            latitude,
            longitude
        )

        if (
            shortest_distance is None
            or distance < shortest_distance
        ):

            shortest_distance = distance

            nearest_ambulance = dict(
                ambulance
            )

            nearest_ambulance[
                "distance_km"
            ] = distance

    return nearest_ambulance


# =========================================================
# CREATE AMBULANCE REQUEST
# =========================================================

def create_ambulance_request(
    patient_user_id: int,
    latitude: float,
    longitude: float,
    emergency_type: str = "medical",
    requested_by_user_id: int | None = None
) -> dict:

    if not validate_location(
        latitude,
        longitude
    ):

        raise ValueError(
            "Invalid patient location"
        )

    return {

        "patient_user_id":
            patient_user_id,

        "requested_by_user_id":
            requested_by_user_id,

        "latitude":
            latitude,

        "longitude":
            longitude,

        "emergency_type":
            emergency_type,

        "status":
            "requested",

        "assigned_ambulance_id":
            None
    }


# =========================================================
# ASSIGN AMBULANCE
# =========================================================

def assign_ambulance(
    ambulance: dict,
    request: dict
) -> dict:

    assigned_request = dict(request)

    assigned_request[
        "assigned_ambulance_id"
    ] = ambulance.get("id")

    assigned_request[
        "status"
    ] = "assigned"

    return assigned_request


# =========================================================
# UPDATE AMBULANCE STATUS
# =========================================================

def update_ambulance_status(
    ambulance: dict,
    status: str
) -> dict:

    allowed_statuses = [
        "available",
        "busy",
        "on_trip",
        "offline",
        "maintenance"
    ]

    if status not in allowed_statuses:

        raise ValueError(
            "Invalid ambulance status"
        )

    updated_ambulance = dict(
        ambulance
    )

    updated_ambulance[
        "status"
    ] = status

    return updated_ambulance


# =========================================================
# UPDATE AMBULANCE LOCATION
# =========================================================

def update_ambulance_location(
    ambulance: dict,
    latitude: float,
    longitude: float
) -> dict:

    if not validate_location(
        latitude,
        longitude
    ):

        raise ValueError(
            "Invalid ambulance location"
        )

    updated_ambulance = dict(
        ambulance
    )

    updated_ambulance[
        "latitude"
    ] = latitude

    updated_ambulance[
        "longitude"
    ] = longitude

    return updated_ambulance


# =========================================================
# COMPLETE AMBULANCE REQUEST
# =========================================================

def complete_ambulance_request(
    request: dict
) -> dict:

    completed_request = dict(
        request
    )

    completed_request[
        "status"
    ] = "completed"

    return completed_request


# =========================================================
# CANCEL AMBULANCE REQUEST
# =========================================================

def cancel_ambulance_request(
    request: dict
) -> dict:

    cancelled_request = dict(
        request
    )

    cancelled_request[
        "status"
    ] = "cancelled"

    return cancelled_request