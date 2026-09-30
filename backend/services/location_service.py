# =========================================================
# AROGYABANDHU LOCATION SERVICE
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

    """
    Calculate the approximate distance between
    two GPS coordinates in kilometres.
    """

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

    distance = earth_radius * c

    return round(distance, 2)


# =========================================================
# LOCATION VALIDATION
# =========================================================

def validate_coordinates(
    latitude: float,
    longitude: float
) -> bool:

    if latitude < -90 or latitude > 90:
        return False

    if longitude < -180 or longitude > 180:
        return False

    return True


# =========================================================
# ASHA LOCATION DATA
# =========================================================

def create_location_data(
    user_id: int,
    role: str,
    latitude: float,
    longitude: float,
    accuracy: float | None = None
) -> dict:

    if not validate_coordinates(
        latitude,
        longitude
    ):

        raise ValueError(
            "Invalid latitude or longitude"
        )

    return {

        "user_id": user_id,

        "role": role,

        "latitude": latitude,

        "longitude": longitude,

        "accuracy": accuracy
    }


# =========================================================
# FIND NEARBY ASHA WORKERS
# =========================================================

def find_nearby_workers(
    workers: list,
    patient_latitude: float,
    patient_longitude: float,
    radius_km: float = 10.0
) -> list:

    nearby_workers = []

    for worker in workers:

        worker_latitude = worker.get(
            "latitude"
        )

        worker_longitude = worker.get(
            "longitude"
        )

        if (
            worker_latitude is None
            or worker_longitude is None
        ):
            continue

        distance = calculate_distance(
            patient_latitude,
            patient_longitude,
            worker_latitude,
            worker_longitude
        )

        if distance <= radius_km:

            worker_data = dict(worker)

            worker_data["distance_km"] = distance

            nearby_workers.append(
                worker_data
            )

    nearby_workers.sort(
        key=lambda worker:
        worker["distance_km"]
    )

    return nearby_workers