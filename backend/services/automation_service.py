# =========================================================
# AROGYABANDHU AUTOMATION SERVICE
# =========================================================


# =========================================================
# PRIORITY LEVELS
# =========================================================

PRIORITY_LEVELS = [
    "low",
    "normal",
    "high",
    "urgent"
]


# =========================================================
# CREATE AUTOMATION EVENT
# =========================================================

def create_event(
    event_type: str,
    source: str,
    patient_user_id: int | None = None,
    priority: str = "normal",
    payload: str = ""
) -> dict:

    if priority not in PRIORITY_LEVELS:

        raise ValueError(
            "Invalid priority level"
        )

    return {

        "event_type": event_type,

        "source": source,

        "patient_user_id":
            patient_user_id,

        "priority":
            priority,

        "payload":
            payload,

        "status":
            "new"
    }


# =========================================================
# CREATE AUTOMATION TASK
# =========================================================

def create_task(
    event_id: int | None,
    task_type: str,
    title: str,
    description: str = "",
    assigned_to_user_id: int | None = None,
    due_at=None
) -> dict:

    return {

        "event_id":
            event_id,

        "assigned_to_user_id":
            assigned_to_user_id,

        "task_type":
            task_type,

        "title":
            title,

        "description":
            description,

        "status":
            "pending",

        "due_at":
            due_at
    }


# =========================================================
# CREATE ASHA FOLLOW-UP TASK
# =========================================================

def create_asha_followup_task(
    patient_user_id: int,
    asha_user_id: int,
    reason: str,
    priority: str = "normal"
) -> dict:

    if priority not in PRIORITY_LEVELS:

        raise ValueError(
            "Invalid priority level"
        )

    return {

        "patient_user_id":
            patient_user_id,

        "assigned_to_user_id":
            asha_user_id,

        "task_type":
            "asha_followup",

        "title":
            "Patient Follow-up",

        "description":
            reason,

        "priority":
            priority,

        "status":
            "pending"
    }


# =========================================================
# CREATE DOCTOR FOLLOW-UP TASK
# =========================================================

def create_doctor_followup_task(
    patient_user_id: int,
    doctor_user_id: int,
    reason: str,
    priority: str = "normal"
) -> dict:

    if priority not in PRIORITY_LEVELS:

        raise ValueError(
            "Invalid priority level"
        )

    return {

        "patient_user_id":
            patient_user_id,

        "assigned_to_user_id":
            doctor_user_id,

        "task_type":
            "doctor_followup",

        "title":
            "Doctor Follow-up",

        "description":
            reason,

        "priority":
            priority,

        "status":
            "pending"
    }


# =========================================================
# CREATE REMINDER TASK
# =========================================================

def create_reminder_task(
    patient_user_id: int,
    title: str,
    description: str,
    due_at=None
) -> dict:

    return {

        "patient_user_id":
            patient_user_id,

        "task_type":
            "reminder",

        "title":
            title,

        "description":
            description,

        "status":
            "pending",

        "due_at":
            due_at
    }


# =========================================================
# UPDATE EVENT STATUS
# =========================================================

def update_event_status(
    event: dict,
    status: str
) -> dict:

    allowed_statuses = [
        "new",
        "processing",
        "completed",
        "failed",
        "cancelled"
    ]

    if status not in allowed_statuses:

        raise ValueError(
            "Invalid event status"
        )

    updated_event = dict(
        event
    )

    updated_event[
        "status"
    ] = status

    return updated_event


# =========================================================
# UPDATE TASK STATUS
# =========================================================

def update_task_status(
    task: dict,
    status: str
) -> dict:

    allowed_statuses = [
        "pending",
        "in_progress",
        "completed",
        "cancelled"
    ]

    if status not in allowed_statuses:

        raise ValueError(
            "Invalid task status"
        )

    updated_task = dict(
        task
    )

    updated_task[
        "status"
    ] = status

    return updated_task


# =========================================================
# PRIORITY DECISION
# =========================================================

def determine_priority(
    emergency_flag: bool = False,
    followup_required: bool = False,
    missed_appointment: bool = False
) -> str:

    if emergency_flag:

        return "urgent"

    if followup_required:

        return "high"

    if missed_appointment:

        return "normal"

    return "low"


# =========================================================
# AUTOMATION WORKFLOW
# =========================================================

def create_workflow(
    patient_user_id: int,
    event_type: str,
    source: str,
    reason: str = "",
    emergency_flag: bool = False,
    followup_required: bool = False,
    missed_appointment: bool = False
) -> dict:

    priority = determine_priority(
        emergency_flag=emergency_flag,
        followup_required=followup_required,
        missed_appointment=missed_appointment
    )

    event = create_event(
        event_type=event_type,
        source=source,
        patient_user_id=patient_user_id,
        priority=priority,
        payload=reason
    )

    task = create_task(
        event_id=None,
        task_type="healthcare_workflow",
        title="Healthcare Follow-up",
        description=reason
    )

    return {

        "event":
            event,

        "task":
            task,

        "priority":
            priority
    }