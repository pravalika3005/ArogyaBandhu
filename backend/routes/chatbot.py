# =========================================================
# AROGYABANDHU AI CHATBOT ROUTES
# =========================================================

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import (
    ChatConversation,
    ChatMessage
)

from ai_chatbot import generate_response


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/api/chatbot",
    tags=["AI Chatbot"]
)


# =========================================================
# REQUEST MODELS
# =========================================================

class ChatRequest(BaseModel):

    user_id: int | None = None

    conversation_id: int | None = None

    message: str

    language: str = "english"


class ConversationRequest(BaseModel):

    user_id: int | None = None

    language: str = "english"


# =========================================================
# CREATE CONVERSATION
# =========================================================

@router.post("/conversation")
def create_conversation(
    request: ConversationRequest,
    db: Session = Depends(get_db)
):

    conversation = ChatConversation(

        user_id=request.user_id,

        language=request.language,

        status="active"
    )

    db.add(conversation)

    db.commit()

    db.refresh(conversation)

    return {

        "message":
            "Chat conversation created",

        "conversation_id":
            conversation.id
    }


# =========================================================
# SEND CHAT MESSAGE
# =========================================================

@router.post("/message")
def send_message(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    message = request.message.strip()

    if not message:

        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )


    # Generate AI response

    ai_result = generate_response(

        message=message,

        language=request.language
    )


    if request.conversation_id is not None:

        conversation = (
            db.query(ChatConversation)
            .filter(
                ChatConversation.id
                == request.conversation_id
            )
            .first()
        )

        if (
            not conversation
            or conversation.user_id != request.user_id
        ):

            raise HTTPException(
                status_code=404,
                detail="Conversation not found"
            )

        if conversation.status != "active":

            raise HTTPException(
                status_code=400,
                detail="Conversation is closed"
            )

        conversation.language = ai_result["language"]

    else:

        conversation = ChatConversation(
            user_id=request.user_id,
            language=ai_result["language"],
            status="active"
        )

        db.add(conversation)

        db.flush()


    # Store user message

    user_message = ChatMessage(

        conversation_id=
            conversation.id,

        sender_type=
            "user",

        message=
            message
    )

    db.add(user_message)


    # Store AI response

    assistant_message = ChatMessage(

        conversation_id=
            conversation.id,

        sender_type=
            "assistant",

        message=
            ai_result["response"]
    )

    db.add(assistant_message)

    db.commit()

    db.refresh(conversation)


    return {

        "conversation_id":
            conversation.id,

        "message":
            ai_result["response"],

        "topic":
            ai_result["topic"],

        "language":
            ai_result["language"],

        "is_diagnosis":
            ai_result["is_diagnosis"],

        "disclaimer":
            ai_result["disclaimer"]
    }


# =========================================================
# GET CONVERSATION
# =========================================================

@router.get("/conversation/{conversation_id}")
def get_conversation(
    conversation_id: int,
    user_id: int | None = None,
    db: Session = Depends(get_db)
):

    conversation = (
        db.query(ChatConversation)
        .filter(
            ChatConversation.id
            == conversation_id
        )
        .first()
    )


    if not conversation:

        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    if (
        user_id is not None
        and conversation.user_id != user_id
    ):

        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )


    messages = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.conversation_id
            == conversation_id
        )
        .order_by(
            ChatMessage.created_at.asc()
        )
        .all()
    )


    return {

        "conversation": {

            "id":
                conversation.id,

            "user_id":
                conversation.user_id,

            "language":
                conversation.language,

            "status":
                conversation.status
        },

        "messages":
            messages
    }


# =========================================================
# GET USER CONVERSATIONS
# =========================================================

@router.get("/user/{user_id}")
def get_user_conversations(
    user_id: int,
    db: Session = Depends(get_db)
):

    conversations = (
        db.query(ChatConversation)
        .filter(
            ChatConversation.user_id
            == user_id
        )
        .order_by(
            ChatConversation.created_at.desc()
        )
        .all()
    )


    return {

        "user_id":
            user_id,

        "conversations":
            conversations
    }


# =========================================================
# CLOSE CONVERSATION
# =========================================================

@router.put(
    "/conversation/{conversation_id}/close"
)
def close_conversation(
    conversation_id: int,
    user_id: int | None = None,
    db: Session = Depends(get_db)
):

    conversation = (
        db.query(ChatConversation)
        .filter(
            ChatConversation.id
            == conversation_id
        )
        .first()
    )


    if not conversation:

        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    if (
        user_id is not None
        and conversation.user_id != user_id
    ):

        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )


    conversation.status = "closed"

    db.commit()

    db.refresh(conversation)


    return {

        "message":
            "Conversation closed successfully",

        "conversation_id":
            conversation.id,

        "status":
            conversation.status
    }