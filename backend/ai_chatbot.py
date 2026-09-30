# =========================================================
# AROGYABANDHU AI CHATBOT SERVICE
# =========================================================

from typing import Dict


# =========================================================
# HEALTH INFORMATION
# =========================================================

HEALTH_RESPONSES = {

    "fever": {
        "english":
            "Fever can have many causes. Rest, drink safe fluids, "
            "and monitor your symptoms. If the fever is severe or "
            "persistent, contact a qualified healthcare professional.",

        "telugu":
            "జ్వరానికి అనేక కారణాలు ఉండవచ్చు. విశ్రాంతి తీసుకోండి "
            "మరియు సురక్షితమైన ద్రవాలు తీసుకోండి. జ్వరం ఎక్కువగా "
            "ఉంటే లేదా ఎక్కువసేపు కొనసాగితే ఆరోగ్య నిపుణులను సంప్రదించండి.",

        "hindi":
            "बुखार के कई कारण हो सकते हैं। आराम करें और सुरक्षित "
            "तरल पदार्थ लें। यदि बुखार अधिक हो या लंबे समय तक रहे, "
            "तो स्वास्थ्य विशेषज्ञ से संपर्क करें।"
    },

    "headache": {
        "english":
            "Headaches can have different causes. Rest and stay hydrated. "
            "If the headache is sudden, severe, or persistent, seek medical advice.",

        "telugu":
            "తలనొప్పికి అనేక కారణాలు ఉండవచ్చు. విశ్రాంతి తీసుకుని "
            "తగినంత నీరు తాగండి. తలనొప్పి అకస్మాత్తుగా తీవ్రమైతే "
            "లేదా ఎక్కువసేపు కొనసాగితే వైద్య సలహా తీసుకోండి.",

        "hindi":
            "सिरदर्द के कई कारण हो सकते हैं। आराम करें और पर्याप्त "
            "पानी पिएं। यदि सिरदर्द अचानक बहुत तेज हो या लंबे समय तक "
            "रहे, तो चिकित्सा सलाह लें।"
    },

    "cough": {
        "english":
            "A cough can have several causes. Stay hydrated and avoid "
            "smoke or other irritants. Seek medical advice if symptoms "
            "are severe or persistent.",

        "telugu":
            "దగ్గుకు అనేక కారణాలు ఉండవచ్చు. తగినంత ద్రవాలు తీసుకోండి "
            "మరియు పొగను నివారించండి. లక్షణాలు తీవ్రమైతే లేదా ఎక్కువసేపు "
            "కొనసాగితే వైద్య సలహా తీసుకోండి.",

        "hindi":
            "खांसी के कई कारण हो सकते हैं। पर्याप्त तरल पदार्थ लें "
            "और धुएं से बचें। लक्षण गंभीर या लंबे समय तक रहने पर "
            "चिकित्सकीय सलाह लें।"
    },

    "stomach": {
        "english":
            "Stomach discomfort can have different causes. Drink safe "
            "fluids and choose light foods if tolerated. Severe pain "
            "or repeated vomiting requires medical attention.",

        "telugu":
            "కడుపు అసౌకర్యానికి అనేక కారణాలు ఉండవచ్చు. సురక్షితమైన "
            "ద్రవాలు తీసుకోండి మరియు తేలికపాటి ఆహారం తీసుకోండి. "
            "తీవ్రమైన నొప్పి లేదా పదేపదే వాంతులు ఉంటే వైద్య సహాయం తీసుకోండి.",

        "hindi":
            "पेट की परेशानी के कई कारण हो सकते हैं। सुरक्षित तरल पदार्थ "
            "लें और हल्का भोजन करें। तेज दर्द या बार-बार उल्टी होने पर "
            "चिकित्सकीय सहायता लें।"
    },

    "food": {
        "english":
            "A balanced diet can include vegetables, fruits, whole grains, "
            "protein-rich foods, and safe drinking water.",

        "telugu":
            "సమతుల్య ఆహారంలో కూరగాయలు, పండ్లు, సంపూర్ణ ధాన్యాలు, "
            "ప్రోటీన్ ఉన్న ఆహారం మరియు సురక్షితమైన తాగునీరు ఉండవచ్చు.",

        "hindi":
            "संतुलित आहार में सब्जियां, फल, साबुत अनाज, प्रोटीन युक्त "
            "खाद्य पदार्थ और सुरक्षित पेयजल शामिल हो सकते हैं।"
    }
}


# =========================================================
# DEFAULT RESPONSE
# =========================================================

DEFAULT_RESPONSES = {

    "english":
        "I can provide general health information. "
        "I do not diagnose medical conditions. "
        "For serious or worsening symptoms, please contact "
        "a qualified healthcare professional.",

    "telugu":
        "నేను సాధారణ ఆరోగ్య సమాచారాన్ని అందించగలను. "
        "నేను వ్యాధులను నిర్ధారించను. తీవ్రమైన లేదా "
        "ఎక్కువవుతున్న లక్షణాలు ఉంటే ఆరోగ్య నిపుణులను సంప్రదించండి.",

    "hindi":
        "मैं सामान्य स्वास्थ्य जानकारी प्रदान कर सकता हूं। "
        "मैं बीमारी का निदान नहीं करता। गंभीर या बढ़ते लक्षणों "
        "के लिए स्वास्थ्य विशेषज्ञ से संपर्क करें।"
}


# =========================================================
# LANGUAGE VALIDATION
# =========================================================

def get_language(language: str) -> str:

    language = language.lower().strip()

    if language not in [
        "english",
        "telugu",
        "hindi"
    ]:
        return "english"

    return language


# =========================================================
# FIND HEALTH TOPIC
# =========================================================

def detect_topic(message: str) -> str:

    message = message.lower().strip()

    if "fever" in message or "జ్వరం" in message:
        return "fever"

    if (
        "headache" in message
        or "head pain" in message
        or "తలనొప్పి" in message
    ):
        return "headache"

    if "cough" in message or "దగ్గు" in message:
        return "cough"

    if (
        "stomach" in message
        or "abdomen" in message
        or "stomach pain" in message
        or "కడుపు" in message
    ):
        return "stomach"

    if (
        "food" in message
        or "diet" in message
        or "healthy food" in message
        or "ఆహారం" in message
    ):
        return "food"

    return "general"


# =========================================================
# GENERATE CHATBOT RESPONSE
# =========================================================

def generate_response(
    message: str,
    language: str = "english"
) -> Dict:

    selected_language = get_language(language)

    topic = detect_topic(message)

    if topic in HEALTH_RESPONSES:

        response = HEALTH_RESPONSES[
            topic
        ][selected_language]

    else:

        response = DEFAULT_RESPONSES[
            selected_language
        ]


    return {

        "response": response,

        "topic": topic,

        "language": selected_language,

        "is_diagnosis": False,

        "disclaimer":
            "This AI assistant provides general health information "
            "and does not diagnose medical conditions."
    }