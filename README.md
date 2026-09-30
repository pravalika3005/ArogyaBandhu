# ArogyaBandhu – Rural Healthcare Support System

## 📌 Overview

ArogyaBandhu is a rural healthcare support platform designed to improve access to essential healthcare services for people living in rural and underserved areas.

The system connects patients with healthcare resources such as emergency assistance, ASHA workers, health records, medicine availability, online consultation, health education, and an AI-powered symptom assistant.

## 🎯 Problem Statement

People in rural areas may face difficulties accessing doctors, emergency services, medicines, health information, and proper medical guidance.

ArogyaBandhu aims to provide these services through a single, simple and accessible digital platform.

## 💡 Proposed Solution

ArogyaBandhu provides:

* 🚑 Emergency assistance
* 👩‍⚕️ ASHA worker support
* 🏥 Ambulance assistance
* 📋 Digital health records
* 💊 Medicine shop search
* 👨‍⚕️ Online consultation
* 🤖 AI symptom assistant
* 🗣️ Voice-based interaction
* 🌐 Multiple-language support
* 📚 Health education and awareness
* 📍 Location-based healthcare assistance

## 🚀 Core Modules

### 1. User & Patient Profile

Stores basic patient information and healthcare-related details.

### 2. Emergency Helpline

Helps users quickly contact emergency contacts, ASHA workers and ambulance services.

### 3. ASHA Worker Location & Assistance

Uses location-based functionality to identify and connect users with nearby ASHA workers.

### 4. Health Records

Allows users to maintain and view their health information and updates.

### 5. Medicine Search

Helps users locate nearby medicine shops and check medicine availability.

### 6. Online Consultation

Provides a platform for users to connect with healthcare professionals remotely.

### 7. AI Symptom Assistant

Allows users to describe symptoms using text or voice and receive general health guidance.

> The AI assistant is intended for preliminary guidance and does not replace professional medical diagnosis.

### 8. Health Education

Provides simple health information using categories, visuals and regional-language support.

### 9. Location Services

Uses GPS/location services to support emergency response, ASHA worker discovery and nearby healthcare services.

### 10. Automation & Notifications

Provides automated alerts and notifications for emergency situations, healthcare updates and important reminders.

## 🛠️ Technology Stack

### Frontend

* Flutter
* Dart

### Backend

* Python
* FastAPI

### Database & Cloud

* Firebase
* Firebase Authentication
* Cloud Firestore

### AI

* Python
* Machine Learning / AI models
* AI chatbot

### APIs & Services

* Location/GPS APIs
* Maps API
* Emergency communication services
* Video consultation services

## 📁 Project Structure

```text
ArogyaBandhu/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── routes/
│   ├── models/
│   ├── services/
│   └── utils/
│
├── frontend/
│   └── Flutter application
│
├── dataset/
│
├── README.md
├── .gitignore
└── .env.example
```

## ⚙️ Installation

### Backend

```bash
cd backend

python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI server:

```bash
uvicorn main:app --reload
```

### Frontend

Open the Flutter project and run:

```bash
flutter pub get
flutter run
```

## 🔐 Environment Variables

Create a `.env` file for sensitive configuration.

Example:

```env
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_API_KEY=your_api_key
MAPS_API_KEY=your_maps_api_key
```

Never upload the real `.env` file or Firebase private credentials to GitHub.

## 🔮 Future Scope

* Regional-language AI voice assistant
* Improved symptom-analysis models
* Real-time ASHA worker tracking
* Ambulance dispatch integration
* Telemedicine integration
* Predictive healthcare analytics
* Offline-first rural functionality
* Government healthcare-service integration

## ⚠️ Disclaimer

ArogyaBandhu is an educational/prototype healthcare technology project. Information provided by the AI assistant should not be treated as a medical diagnosis or a substitute for professional medical advice.

## 👩‍💻 Project

**ArogyaBandhu – Rural Healthcare Support System**

Developed as a student project focused on improving healthcare accessibility in rural communities.
cd "c:\Users\Pravalika\OneDrive\Desktop\rural-healthcare-system\frontend"
flutter pub get
flutter run
```"

Need maybe note "The warnings are resolved." Good.



Fixed the missing route modules that were causing the project to fail resolution in VS Code.

I added:
- `backend/routes/auth.py`
- `backend/routes/pharmacy.py`

and the backend now starts and responds correctly.

Validated:
- Backend starts with Uvicorn
- `/`, `/auth/login`, `/pharmacy/` respond successfully
- Flutter analysis: “No issues found!”
- Flutter tests: “All tests passed!”

Run it:

```powershell
cd "c:\Users\Pravalika\OneDrive\Desktop\rural-healthcare-system\backend"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000