from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import engine, get_db
from models import Base, User

# -----------------------------
# Import API Routers
# -----------------------------

from routes.patients import router as patients_router
from routes.doctors import router as doctors_router
from routes.asha import router as asha_router
from routes.pharmcy import router as pharmacy_router
from routes.appointments import router as appointments_router
from routes.chatbot import router as chatbot_router
from routes.location import router as location_router
from routes.notifications import router as notifications_router
from routes.automation import router as automation_router
from routes.profile import router as profile_router


# -----------------------------
# Create Database Tables
# -----------------------------

Base.metadata.create_all(bind=engine)


# -----------------------------
# FastAPI Application
# -----------------------------

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "templates" / "arogyabhandhu"

app = FastAPI(
    title="ArogyaBandhu API",
    description=(
        "AI-powered rural healthcare platform connecting "
        "patients, doctors, ASHA workers, pharmacies and "
        "emergency support."
    ),
    version="1.0.0"
)


# -----------------------------
# CORS Configuration
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Password Security
# -----------------------------

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# -----------------------------
# Basic Request Models
# -----------------------------

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str = "patient"


class LoginRequest(BaseModel):
    email: str
    password: str


class ChatRequest(BaseModel):
    message: str
    language: str = "English"


class EmergencyRequest(BaseModel):
    user_id: int | None = None
    latitude: float | None = None
    longitude: float | None = None
    emergency_type: str = "medical_emergency"


# -----------------------------
# Health Information
# -----------------------------

def health_response(
    language: str,
    topic: str
):
    language = language.lower()
    topic = topic.lower()

    responses = {

        "fever": {
            "english": (
                "For a fever, rest, drink enough fluids and monitor "
                "your temperature. If the fever is severe, persistent, "
                "or accompanied by serious symptoms, seek medical care."
            ),
            "telugu": (
                "జ్వరం ఉన్నప్పుడు విశ్రాంతి తీసుకోండి, తగినంత నీరు "
                "తాగండి మరియు శరీర ఉష్ణోగ్రతను గమనించండి. జ్వరం "
                "తీవ్రంగా లేదా ఎక్కువకాలం ఉంటే వైద్యుడిని సంప్రదించండి."
            ),
            "hindi": (
                "बुखार होने पर आराम करें, पर्याप्त पानी पिएं और "
                "तापमान पर नजर रखें। यदि बुखार तेज या लगातार रहे "
                "या गंभीर लक्षण हों तो डॉक्टर से संपर्क करें।"
            )
        },

        "headache": {
            "english": (
                "For a mild headache, rest, stay hydrated and avoid "
                "excessive screen exposure. Severe, sudden or recurring "
                "headaches should be evaluated by a healthcare professional."
            ),
            "telugu": (
                "తేలికపాటి తలనొప్పి ఉంటే విశ్రాంతి తీసుకోండి, తగినంత "
                "నీరు తాగండి మరియు ఎక్కువ స్క్రీన్ వినియోగాన్ని తగ్గించండి. "
                "తీవ్రమైన లేదా తరచుగా వచ్చే తలనొప్పికి వైద్యుడిని సంప్రదించండి."
            ),
            "hindi": (
                "हल्के सिरदर्द में आराम करें, पर्याप्त पानी पिएं और "
                "अधिक स्क्रीन समय से बचें। तेज या बार-बार होने वाले "
                "सिरदर्द के लिए डॉक्टर से संपर्क करें।"
            )
        },

        "cough": {
            "english": (
                "For a mild cough, stay hydrated and rest. Avoid smoke "
                "and other irritants. Seek medical care if breathing "
                "difficulty, chest pain or persistent symptoms occur."
            ),
            "telugu": (
                "తేలికపాటి దగ్గు ఉంటే నీరు తాగుతూ విశ్రాంతి తీసుకోండి. "
                "పొగ మరియు ఇతర ఇబ్బందికరమైన పదార్థాలను నివారించండి. "
                "శ్వాస తీసుకోవడంలో ఇబ్బంది ఉంటే వైద్య సహాయం పొందండి."
            ),
            "hindi": (
                "हल्की खांसी में पर्याप्त पानी पिएं और आराम करें। "
                "धुएं और अन्य परेशान करने वाली चीजों से बचें। "
                "सांस लेने में कठिनाई होने पर चिकित्सा सहायता लें।"
            )
        },

        "stomach": {
            "english": (
                "For mild stomach discomfort, drink fluids and choose "
                "light foods. Avoid foods that make the symptoms worse. "
                "Severe or persistent abdominal pain needs medical attention."
            ),
            "telugu": (
                "తేలికపాటి కడుపు అసౌకర్యం ఉంటే ద్రవాలు తీసుకోండి మరియు "
                "తేలికపాటి ఆహారం తీసుకోండి. తీవ్రమైన లేదా ఎక్కువకాలం "
                "కొనసాగే కడుపు నొప్పికి వైద్యుడిని సంప్రదించండి."
            ),
            "hindi": (
                "हल्की पेट की परेशानी में पर्याप्त तरल पदार्थ लें और "
                "हल्का भोजन करें। तेज या लगातार पेट दर्द होने पर "
                "डॉक्टर से संपर्क करें।"
            )
        },

        "food": {
            "english": (
                "A balanced diet can include vegetables, fruits, "
                "whole grains, pulses and suitable protein sources. "
                "Drink enough safe water."
            ),
            "telugu": (
                "సమతుల్య ఆహారంలో కూరగాయలు, పండ్లు, సంపూర్ణ ధాన్యాలు, "
                "పప్పులు మరియు తగిన ప్రోటీన్ వనరులు ఉండవచ్చు. "
                "సురక్షితమైన నీటిని తగినంతగా తాగండి."
            ),
            "hindi": (
                "संतुलित आहार में सब्जियां, फल, साबुत अनाज, दालें "
                "और उचित प्रोटीन स्रोत शामिल किए जा सकते हैं। "
                "पर्याप्त सुरक्षित पानी पिएं।"
            )
        }
    }

    selected_language = language

    if selected_language not in [
        "english",
        "telugu",
        "hindi"
    ]:
        selected_language = "english"

    if topic in responses:
        return responses[topic][selected_language]

    return (
        "I can provide general health information, but I cannot "
        "diagnose a medical condition. For serious or persistent "
        "symptoms, please consult a qualified healthcare professional."
    )


# -----------------------------
# Root Endpoint
# -----------------------------

@app.get("/")
def root():
    return FileResponse(FRONTEND_DIR / "index.html")


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ArogyaBandhu API"
    }


# ============================================================
# FRONTEND COMPATIBILITY ENDPOINTS
# ============================================================

# -----------------------------
# Register
# -----------------------------

@app.post("/api/register")
def register_user(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    if len(request.password) < 6:
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least 6 characters"
        )

    allowed_roles = [
        "patient",
        "doctor",
        "asha",
        "pharmacy"
    ]

    if request.role not in allowed_roles:
        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    existing_user = db.query(User).filter(
        User.email == request.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = pwd_context.hash(
        request.password
    )

    user = User(
        name=request.name,
        email=request.email,
        password_hash=hashed_password,
        role=request.role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Registration successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }


# -----------------------------
# Login
# -----------------------------

@app.post("/api/login")
def login_user(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == request.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Account is inactive"
        )

    try:
        password_valid = pwd_context.verify(
            request.password,
            user.password_hash
        )
    except Exception:
        password_valid = False

    if not password_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }


# -----------------------------
# Simple Chat Compatibility API
# -----------------------------

@app.post("/api/chat")
def chat(
    request: ChatRequest
):
    message = request.message.lower()

    topic = "general"

    if any(word in message for word in [
        "fever",
        "temperature",
        "జ్వరం",
        "बुखार"
    ]):
        topic = "fever"

    elif any(word in message for word in [
        "headache",
        "head pain",
        "తలనొప్పి",
        "सिरदर्द"
    ]):
        topic = "headache"

    elif any(word in message for word in [
        "cough",
        "దగ్గు",
        "खांसी"
    ]):
        topic = "cough"

    elif any(word in message for word in [
        "stomach",
        "abdominal",
        "కడుపు",
        "पेट"
    ]):
        topic = "stomach"

    elif any(word in message for word in [
        "food",
        "diet",
        "nutrition",
        "ఆహారం",
        "भोजन"
    ]):
        topic = "food"

    response = health_response(
        request.language,
        topic
    )

    return {
        "message": response,
        "topic": topic,
        "language": request.language,
        "is_diagnosis": False,
        "disclaimer": (
            "This AI assistant provides general health information "
            "and does not provide medical diagnosis."
        )
    }


# -----------------------------
# Emergency Compatibility API
# -----------------------------

@app.post("/api/emergency")
def emergency(
    request: EmergencyRequest
):
    location = None

    if (
        request.latitude is not None
        and request.longitude is not None
    ):
        location = {
            "latitude": request.latitude,
            "longitude": request.longitude
        }

    return {
        "message": "Emergency request received",
        "emergency_type": request.emergency_type,
        "user_id": request.user_id,
        "location": location,
        "status": "received",
        "prototype_notice": (
            "This prototype does not directly dispatch a real "
            "ambulance. In an actual deployment, this module "
            "would connect to an authorized emergency service."
        ),
        "emergency_numbers": [
            "112",
            "108"
        ]
    }


# ============================================================
# INCLUDE ALL ROUTERS
# ============================================================

app.include_router(patients_router)
app.include_router(doctors_router)
app.include_router(asha_router)
app.include_router(pharmacy_router)
app.include_router(appointments_router)
app.include_router(chatbot_router)
app.include_router(location_router)
app.include_router(notifications_router)
app.include_router(automation_router)
app.include_router(profile_router)

app.mount(
    "/css",
    StaticFiles(directory=FRONTEND_DIR.parent / "css"),
    name="styles"
)
app.mount(
    "/js",
    StaticFiles(directory=FRONTEND_DIR.parent / "js"),
    name="scripts"
)
app.mount(
    "/images",
    StaticFiles(directory=FRONTEND_DIR.parent / "images"),
    name="images"
)
app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="website"
)
