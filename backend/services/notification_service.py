# =========================================================
# AROGYABANDHU NOTIFICATION SERVICE
# =========================================================


# =========================================================
# CREATE NOTIFICATION
# =========================================================

def create_notification(
    user_id: int,
    title: str,
    message: str,
    notification_type: str = "general"
) -> dict:

    return {

        "user_id":
            user_id,

        "title":
            title,

        "message":
            message,

        "notification_type":
            notification_type,

        "is_read":
            False
    }


# =========================================================
# APPOINTMENT NOTIFICATION
# =========================================================

def appointment_notification(
    user_id: int,
    doctor_name: str,
    appointment_time,
    status: str
) -> dict:

    return create_notification(

        user_id=user_id,

        title="Appointment Update",

        message=(
            f"Your appointment with Dr. {doctor_name} "
            f"is {status}."
        ),

        notification_type="appointment"
    )


# =========================================================
# ASHA NOTIFICATION
# =========================================================

def asha_notification(
    user_id: int,
    patient_name: str,
    notification_message: str
) -> dict:

    return create_notification(

        user_id=user_id,

        title="ASHA Health Update",

        message=(
            f"Patient {patient_name}: "
            f"{notification_message}"
        ),

        notification_type="asha"
    )


# =========================================================
# AMBULANCE NOTIFICATION
# =========================================================

def ambulance_notification(
    user_id: int,
    status: str,
    ambulance_number: str = ""
) -> dict:

    if ambulance_number:

        message = (
            f"Ambulance {ambulance_number} "
            f"status: {status}."
        )

    else:

        message = (
            f"Ambulance request status: {status}."
        )

    return create_notification(

        user_id=user_id,

        title="Ambulance Update",

        message=message,

        notification_type="ambulance"
    )


# =========================================================
# MEDICINE ORDER NOTIFICATION
# =========================================================

def medicine_notification(
    user_id: int,
    medicine_name: str,
    status: str
) -> dict:

    return create_notification(

        user_id=user_id,

        title="Medicine Order Update",

        message=(
            f"Your medicine order for "
            f"{medicine_name} is {status}."
        ),

        notification_type="medicine"
    )


# =========================================================
# CHATBOT / AI NOTIFICATION
# =========================================================

def ai_notification(
    user_id: int,
    message: str
) -> dict:

    return create_notification(

        user_id=user_id,

        title="Health Assistant",

        message=message,

        notification_type="ai"
    )


# =========================================================
# AUTOMATION NOTIFICATION
# =========================================================

def automation_notification(
    user_id: int,
    task_title: str,
    task_message: str
) -> dict:

    return create_notification(

        user_id=user_id,

        title=task_title,

        message=task_message,

        notification_type="automation"
    )


# =========================================================
# MARK NOTIFICATION AS READ
# =========================================================

def mark_as_read(
    notification: dict
) -> dict:

    updated_notification = dict(
        notification
    )

    updated_notification[
        "is_read"
    ] = True

    return updated_notification


# =========================================================
# MARK ALL NOTIFICATIONS AS READ
# =========================================================

def mark_all_as_read(
    notifications: list
) -> list:

    updated_notifications = []

    for notification in notifications:

        updated_notification = dict(
            notification
        )

        updated_notification[
            "is_read"
        ] = True

        updated_notifications.append(
            updated_notification
        )

    return updated_notifications


# =========================================================
# FILTER UNREAD NOTIFICATIONS
# =========================================================

def get_unread_notifications(
    notifications: list
) -> list:

    unread_notifications = []

    for notification in notifications:

        if not notification.get(
            "is_read",
            False
        ):

            unread_notifications.append(
                dict(notification)
            )

    return unread_notifications