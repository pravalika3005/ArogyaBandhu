from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import User, AutomationEvent, AutomationTask
from services.automation_service import (
    create_event,
    create_task,
    create_asha_followup_task,
    create_doctor_followup_task,
    create_reminder_task,
    update_event_status,
    update_task_status,
    determine_priority,
    create_workflow
)


router = APIRouter(
    prefix="/api/automation",
    tags=["Automation"]
)


# -----------------------------
# Request Models
# -----------------------------

class EventRequest(BaseModel):
    user_id: int
    event_type: str
    description: str
    priority: str = "normal"


class TaskRequest(BaseModel):
    user_id: int
    task_type: str
    title: str
    description: str = ""
    priority: str = "normal"


class StatusRequest(BaseModel):
    status: str


class PriorityRequest(BaseModel):
    risk_level: str
    urgency: str = "normal"


class WorkflowRequest(BaseModel):
    user_id: int
    workflow_type: str
    description: str = ""


# -----------------------------
# Create Automation Event
# -----------------------------

@router.post("/events")
def create_automation_event(
    request: EventRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == request.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    event = create_event(
        db=db,
        user_id=request.user_id,
        event_type=request.event_type,
        description=request.description,
        priority=request.priority
    )

    return {
        "message": "Automation event created",
        "event": {
            "id": event.id,
            "user_id": event.user_id,
            "event_type": event.event_type,
            "description": event.description,
            "priority": event.priority,
            "status": event.status,
            "created_at": event.created_at
        }
    }


# -----------------------------
# Get User Events
# -----------------------------

@router.get("/events/{user_id}")
def get_user_events(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    events = (
        db.query(AutomationEvent)
        .filter(AutomationEvent.user_id == user_id)
        .order_by(AutomationEvent.created_at.desc())
        .all()
    )

    return {
        "user_id": user_id,
        "count": len(events),
        "events": [
            {
                "id": event.id,
                "event_type": event.event_type,
                "description": event.description,
                "priority": event.priority,
                "status": event.status,
                "created_at": event.created_at
            }
            for event in events
        ]
    }


# -----------------------------
# Update Event Status
# -----------------------------

@router.put("/events/{event_id}/status")
def change_event_status(
    event_id: int,
    request: StatusRequest,
    db: Session = Depends(get_db)
):
    event = update_event_status(
        db=db,
        event_id=event_id,
        status=request.status
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Automation event not found"
        )

    return {
        "message": "Event status updated",
        "event": {
            "id": event.id,
            "status": event.status
        }
    }


# -----------------------------
# Create General Task
# -----------------------------

@router.post("/tasks")
def create_automation_task(
    request: TaskRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == request.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    task = create_task(
        db=db,
        user_id=request.user_id,
        task_type=request.task_type,
        title=request.title,
        description=request.description,
        priority=request.priority
    )

    return {
        "message": "Automation task created",
        "task": {
            "id": task.id,
            "user_id": task.user_id,
            "task_type": task.task_type,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "status": task.status,
            "created_at": task.created_at
        }
    }


# -----------------------------
# Get User Tasks
# -----------------------------

@router.get("/tasks/{user_id}")
def get_user_tasks(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    tasks = (
        db.query(AutomationTask)
        .filter(AutomationTask.user_id == user_id)
        .order_by(AutomationTask.created_at.desc())
        .all()
    )

    return {
        "user_id": user_id,
        "count": len(tasks),
        "tasks": [
            {
                "id": task.id,
                "task_type": task.task_type,
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "status": task.status,
                "created_at": task.created_at
            }
            for task in tasks
        ]
    }


# -----------------------------
# Update Task Status
# -----------------------------

@router.put("/tasks/{task_id}/status")
def change_task_status(
    task_id: int,
    request: StatusRequest,
    db: Session = Depends(get_db)
):
    task = update_task_status(
        db=db,
        task_id=task_id,
        status=request.status
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Automation task not found"
        )

    return {
        "message": "Task status updated",
        "task": {
            "id": task.id,
            "status": task.status
        }
    }


# -----------------------------
# ASHA Follow-up Automation
# -----------------------------

@router.post("/asha-followup")
def asha_followup(
    user_id: int,
    patient_id: int,
    description: str = "",
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="ASHA user not found"
        )

    task = create_asha_followup_task(
        db=db,
        user_id=user_id,
        patient_id=patient_id,
        description=description
    )

    return {
        "message": "ASHA follow-up task created",
        "task": {
            "id": task.id,
            "title": task.title,
            "status": task.status,
            "priority": task.priority
        }
    }


# -----------------------------
# Doctor Follow-up Automation
# -----------------------------

@router.post("/doctor-followup")
def doctor_followup(
    user_id: int,
    patient_id: int,
    description: str = "",
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Doctor user not found"
        )

    task = create_doctor_followup_task(
        db=db,
        user_id=user_id,
        patient_id=patient_id,
        description=description
    )

    return {
        "message": "Doctor follow-up task created",
        "task": {
            "id": task.id,
            "title": task.title,
            "status": task.status,
            "priority": task.priority
        }
    }


# -----------------------------
# Medicine Reminder Automation
# -----------------------------

@router.post("/medicine-reminder")
def medicine_reminder(
    user_id: int,
    medicine_name: str,
    reminder_time: str,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    task = create_reminder_task(
        db=db,
        user_id=user_id,
        medicine_name=medicine_name,
        reminder_time=reminder_time
    )

    return {
        "message": "Medicine reminder created",
        "task": {
            "id": task.id,
            "title": task.title,
            "status": task.status
        }
    }


# -----------------------------
# Determine Workflow Priority
# -----------------------------

@router.post("/priority")
def get_priority(
    request: PriorityRequest
):
    priority = determine_priority(
        risk_level=request.risk_level,
        urgency=request.urgency
    )

    return {
        "risk_level": request.risk_level,
        "urgency": request.urgency,
        "priority": priority
    }


# -----------------------------
# Create Complete Workflow
# -----------------------------

@router.post("/workflow")
def create_automation_workflow(
    request: WorkflowRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == request.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    workflow = create_workflow(
        db=db,
        user_id=request.user_id,
        workflow_type=request.workflow_type,
        description=request.description
    )

    return {
        "message": "Automation workflow created",
        "workflow": workflow
    }