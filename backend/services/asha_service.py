# =========================================================
# AROGYABANDHU ASHA WORKER SERVICE
# =========================================================


# =========================================================
# FIND AVAILABLE ASHA WORKERS
# =========================================================

def get_available_workers(
    workers: list
) -> list:

    available_workers = []

    for worker in workers:

        if worker.get("is_available", False):

            available_workers.append(
                dict(worker)
            )

    return available_workers


# =========================================================
# FIND ASHA WORKERS BY VILLAGE
# =========================================================

def find_workers_by_village(
    workers: list,
    village: str
) -> list:

    village = village.strip().lower()

    matching_workers = []

    for worker in workers:

        worker_village = str(
            worker.get("village", "")
        ).strip().lower()

        if worker_village == village:

            matching_workers.append(
                dict(worker)
            )

    return matching_workers


# =========================================================
# ASSIGN PATIENT TO ASHA WORKER
# =========================================================

def assign_patient(
    asha_user_id: int,
    patient_user_id: int
) -> dict:

    return {

        "asha_user_id":
            asha_user_id,

        "patient_user_id":
            patient_user_id,

        "status":
            "assigned"
    }


# =========================================================
# CREATE ASHA VISIT
# =========================================================

def create_visit(
    asha_user_id: int,
    patient_user_id: int,
    visit_type: str,
    scheduled_at=None,
    notes: str = ""
) -> dict:

    return {

        "asha_user_id":
            asha_user_id,

        "patient_user_id":
            patient_user_id,

        "visit_type":
            visit_type,

        "scheduled_at":
            scheduled_at,

        "notes":
            notes,

        "status":
            "scheduled"
    }


# =========================================================
# UPDATE VISIT STATUS
# =========================================================

def update_visit_status(
    visit: dict,
    status: str
) -> dict:

    allowed_statuses = [
        "scheduled",
        "in_progress",
        "completed",
        "cancelled"
    ]

    if status not in allowed_statuses:

        raise ValueError(
            "Invalid visit status"
        )

    updated_visit = dict(
        visit
    )

    updated_visit[
        "status"
    ] = status

    return updated_visit


# =========================================================
# COMPLETE ASHA VISIT
# =========================================================

def complete_visit(
    visit: dict,
    notes: str = ""
) -> dict:

    completed_visit = dict(
        visit
    )

    completed_visit[
        "status"
    ] = "completed"

    if notes:

        completed_visit[
            "notes"
        ] = notes

    return completed_visit


# =========================================================
# CREATE FAMILY HEALTH TASK
# =========================================================

def create_family_health_task(
    asha_user_id: int,
    patient_user_id: int,
    task_type: str,
    priority: str = "normal"
) -> dict:

    return {

        "asha_user_id":
            asha_user_id,

        "patient_user_id":
            patient_user_id,

        "task_type":
            task_type,

        "priority":
            priority,

        "status":
            "pending"
    }


# =========================================================
# VACCINATION TRACKER
# =========================================================

def create_vaccination_record(
    patient_user_id: int,
    vaccine_name: str,
    scheduled_date=None,
    status: str = "scheduled"
) -> dict:

    allowed_statuses = [
        "scheduled",
        "completed",
        "missed"
    ]

    if status not in allowed_statuses:

        raise ValueError(
            "Invalid vaccination status"
        )

    return {

        "patient_user_id":
            patient_user_id,

        "vaccine_name":
            vaccine_name,

        "scheduled_date":
            scheduled_date,

        "status":
            status
    }


# =========================================================
# MATERNAL HEALTH TRACKER
# =========================================================

def create_maternal_health_record(
    patient_user_id: int,
    pregnancy_stage: str,
    expected_date=None,
    notes: str = ""
) -> dict:

    return {

        "patient_user_id":
            patient_user_id,

        "pregnancy_stage":
            pregnancy_stage,

        "expected_date":
            expected_date,

        "notes":
            notes
    }