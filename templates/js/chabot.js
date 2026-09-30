/* =========================================================
   AROGYABANDHU - CHATBOT.JS
   AI HEALTH ASSISTANT - FRONTEND PROTOTYPE
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    /* =====================================================
       GET HTML ELEMENTS
       ===================================================== */

    const chatForm = document.getElementById("chatForm");

    const chatInput =
        document.getElementById("chatInput");

    const chatMessages =
        document.getElementById("chatMessages");

    const clearChatButton =
        document.getElementById("clearChat");

    const voiceButton =
        document.getElementById("voiceButton");


    /* =====================================================
       CHECK REQUIRED ELEMENTS
       ===================================================== */

    if (!chatForm || !chatInput || !chatMessages) {

        console.error(
            "Chatbot error: Required HTML elements were not found."
        );

        return;
    }


    /* =====================================================
       STORAGE KEY
       ===================================================== */

    const STORAGE_KEY =
        "arogyaBandhuChatHistory";


    /* =====================================================
       EMERGENCY KEYWORDS
       ===================================================== */

    const emergencyKeywords = [

        "chest pain",
        "severe chest pain",
        "difficulty breathing",
        "can't breathe",
        "cannot breathe",
        "breathing problem",
        "unconscious",
        "not responding",
        "severe bleeding",
        "heavy bleeding",
        "stroke",
        "seizure",
        "fits",
        "poisoning",
        "overdose",
        "suicide",
        "self harm",
        "accident",
        "major injury"

    ];


    /* =====================================================
       LOAD CHAT HISTORY
       ===================================================== */

    loadChatHistory();


    /* =====================================================
       INITIAL MESSAGE
       ===================================================== */

    if (
        chatMessages.children.length === 0
    ) {

        addBotMessage(
            "Hello! I am ArogyaBandhu AI Health Assistant. " +
            "Tell me your symptoms, and I can provide general health guidance. " +
            "I cannot diagnose medical conditions."
        );

    }


    /* =====================================================
       FORM SUBMISSION
       ===================================================== */

    chatForm.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();

            const message =
                chatInput.value.trim();


            if (!message) {
                return;
            }


            /* Add user message */

            addUserMessage(message);


            /* Clear input */

            chatInput.value = "";


            /* Show typing indicator */

            showTypingIndicator();


            /* Generate response */

            setTimeout(
                function () {

                    removeTypingIndicator();

                    generateResponse(message);

                },
                700
            );

        }
    );


    /* =====================================================
       CLEAR CHAT
       ===================================================== */

    if (clearChatButton) {

        clearChatButton.addEventListener(
            "click",
            function () {

                localStorage.removeItem(
                    STORAGE_KEY
                );

                chatMessages.innerHTML = "";

                addBotMessage(
                    "Chat cleared. How can I help you today?"
                );

            }
        );

    }


    /* =====================================================
       VOICE INPUT
       ===================================================== */

    if (
        voiceButton &&
        (
            "webkitSpeechRecognition" in window ||
            "SpeechRecognition" in window
        )
    ) {

        const SpeechRecognition =
            window.SpeechRecognition ||
            window.webkitSpeechRecognition;


        const recognition =
            new SpeechRecognition();


        recognition.lang =
            "en-IN";

        recognition.continuous =
            false;

        recognition.interimResults =
            false;


        voiceButton.addEventListener(
            "click",
            function () {

                recognition.start();

            }
        );


        recognition.onresult =
            function (event) {

                const transcript =
                    event.results[0][0].transcript;


                chatInput.value =
                    transcript;

            };


        recognition.onerror =
            function () {

                addBotMessage(
                    "I could not understand the voice input. " +
                    "Please try again or type your message."
                );

            };

    }


    /* =====================================================
       GENERATE RESPONSE
       ===================================================== */

    function generateResponse(message) {

        const text =
            message.toLowerCase();


        /* ---------------------------------------------
           EMERGENCY CHECK
           --------------------------------------------- */

        if (isEmergency(text)) {

            addBotMessage(
                "⚠️ This may require urgent medical attention. " +
                "Please contact emergency services immediately. " +
                "If the patient is in India, call 112 or your local emergency service. " +
                "Do not rely on this chatbot during a medical emergency."
            );

            addEmergencyButton();

            return;
        }


        /* ---------------------------------------------
           GREETING
           --------------------------------------------- */

        if (
            containsAny(
                text,
                [
                    "hello",
                    "hi",
                    "hey",
                    "namaste"
                ]
            )
        ) {

            addBotMessage(
                "Hello! 👋 How are you feeling today? " +
                "You can tell me your symptoms, such as fever, cough, headache, " +
                "stomach pain, or body pain."
            );

            return;
        }


        /* ---------------------------------------------
           FEVER
           --------------------------------------------- */

        if (
            containsAny(
                text,
                [
                    "fever",
                    "temperature",
                    "high temperature"
                ]
            )
        ) {

            addBotMessage(
                "For a fever, rest and drink enough fluids. " +
                "If possible, measure your temperature and monitor how it changes. " +
                "Seek medical advice if the fever is persistent, very high, " +
                "or accompanied by serious symptoms."
            );

            return;
        }


        /* ---------------------------------------------
           COUGH
           --------------------------------------------- */

        if (
            containsAny(
                text,
                [
                    "cough",
                    "coughing"
                ]
            )
        ) {

            addBotMessage(
                "For a mild cough, staying hydrated and getting adequate rest may help. " +
                "Avoid smoke and other irritants. " +
                "If you have breathing difficulty, chest pain, blood in the cough, " +
                "or symptoms that are getting worse, seek medical care."
            );

            return;
        }


        /* ---------------------------------------------
           HEADACHE
           --------------------------------------------- */

        if (
            containsAny(
                text,
                [
                    "headache",
                    "head pain"
                ]
            )
        ) {

            addBotMessage(
                "A headache can have many causes, including dehydration, lack of sleep, " +
                "stress, or illness. Try resting and drinking water. " +
                "If the headache is sudden and extremely severe, follows a serious injury, " +
                "or occurs with weakness, confusion, or vision problems, seek urgent care."
            );

            return;
        }


        /* ---------------------------------------------
           STOMACH PAIN
           --------------------------------------------- */

        if (
            containsAny(
                text,
                [
                    "stomach pain",
                    "stomach ache",
                    "abdominal pain",
                    "belly pain"
                ]
            )
        ) {

            addBotMessage(
                "Stomach pain can have many different causes. " +
                "Avoid foods that clearly worsen your symptoms and stay hydrated. " +
                "If the pain is severe, persistent, or accompanied by repeated vomiting, " +
                "blood, fainting, or severe weakness, seek medical attention."
            );

            return;
        }


        /* ---------------------------------------------
           VOMITING
           --------------------------------------------- */

        if (
            containsAny(
                text,
                [
                    "vomiting",
                    "vomit",
                    "throwing up"
                ]
            )
        ) {

            addBotMessage(
                "If you are vomiting, take small amounts of fluids frequently " +
                "to reduce the risk of dehydration. " +
                "Seek medical care if you cannot keep fluids down, " +
                "have blood in the vomit, severe abdominal pain, or signs of dehydration."
            );

            return;
        }


        /* ---------------------------------------------
           DIARRHEA
           --------------------------------------------- */

        if (
            containsAny(
                text,
                [
                    "diarrhea",
                    "loose motion",
                    "loose motions"
                ]
            )
        ) {

            addBotMessage(
                "Diarrhea can cause dehydration. " +
                "Drink safe fluids and consider oral rehydration solution (ORS). " +
                "Seek medical attention if there is blood in the stool, severe dehydration, " +
                "persistent symptoms, or serious weakness."
            );

            return;
        }


        /* ---------------------------------------------
           COLD
           --------------------------------------------- */

        if (
            containsAny(
                text,
                [
                    "cold",
                    "runny nose",
                    "blocked nose",
                    "stuffy nose"
                ]
            )
        ) {

            addBotMessage(
                "For common cold symptoms, rest, drink fluids, " +
                "and avoid smoke or other irritants. " +
                "If symptoms become severe or you develop breathing difficulty, " +
                "seek medical care."
            );

            return;
        }


        /* ---------------------------------------------
           BODY PAIN
           --------------------------------------------- */

        if (
            containsAny(
                text,
                [
                    "body pain",
                    "body ache",
                    "muscle pain"
                ]
            )
        ) {

            addBotMessage(
                "Body aches can occur with infections, physical strain, " +
                "dehydration, or other conditions. " +
                "Rest and maintain adequate fluid intake. " +
                "If the pain is severe, persistent, or accompanied by serious symptoms, " +
                "consult a healthcare professional."
            );

            return;
        }


        /* ---------------------------------------------
           PREGNANCY
           --------------------------------------------- */

        if (
            containsAny(
                text,
                [
                    "pregnant",
                    "pregnancy",
                    "pregnancy care"
                ]
            )
        ) {

            addBotMessage(
                "Pregnancy requires regular medical care and antenatal check-ups. " +
                "For pregnancy-specific symptoms, medicines, supplements, or concerns, " +
                "please consult a qualified healthcare professional or ASHA worker."
            );

            return;
        }


        /* ---------------------------------------------
           MEDICINE
           --------------------------------------------- */

        if (
            containsAny(
                text,
                [
                    "medicine",
                    "tablet",
                    "medication",
                    "drug"
                ]
            )
        ) {

            addBotMessage(
                "I can provide general information, but I should not prescribe medicines. " +
                "Please use medicines according to a qualified healthcare professional's advice " +
                "or the medicine label."
            );

            return;
        }


        /* ---------------------------------------------
           APPOINTMENT
           --------------------------------------------- */

        if (
            containsAny(
                text,
                [
                    "appointment",
                    "doctor",
                    "consult doctor",
                    "book doctor"
                ]
            )
        ) {

            addBotMessage(
                "You can book a doctor consultation through the " +
                "ArogyaBandhu Appointment section. " +
                "Choose a doctor, date, time, and consultation type."
            );

            addLinkButton(
                "Book Appointment",
                "appointment.html"
            );

            return;
        }


        /* ---------------------------------------------
           HEALTH RECORD
           --------------------------------------------- */

        if (
            containsAny(
                text,
                [
                    "health record",
                    "medical record",
                    "prescription",
                    "lab report"
                ]
            )
        ) {

            addBotMessage(
                "You can manage your prescriptions, medical history, " +
                "lab reports, and other health information through Health Records."
            );

            addLinkButton(
                "Open Health Records",
                "health-record.html"
            );

            return;
        }


        /* ---------------------------------------------
           GENERAL RESPONSE
           --------------------------------------------- */

        addBotMessage(
            "I can provide general information about symptoms, " +
            "appointments, medicines, health records, and basic healthcare guidance. " +
            "Please describe your symptoms clearly, including how long you have had them."
        );

    }


    /* =====================================================
       EMERGENCY DETECTION
       ===================================================== */

    function isEmergency(text) {

        return emergencyKeywords.some(
            function (keyword) {

                return text.includes(keyword);

            }
        );

    }


    /* =====================================================
       CHECK KEYWORDS
       ===================================================== */

    function containsAny(
        text,
        keywords
    ) {

        return keywords.some(
            function (keyword) {

                return text.includes(keyword);

            }
        );

    }


    /* =====================================================
       ADD USER MESSAGE
       ===================================================== */

    function addUserMessage(message) {

        const messageElement =
            document.createElement("div");


        messageElement.className =
            "chat-message user-message";


        messageElement.textContent =
            message;


        chatMessages.appendChild(
            messageElement
        );


        saveMessage(
            "user",
            message
        );


        scrollToBottom();

    }


    /* =====================================================
       ADD BOT MESSAGE
       ===================================================== */

    function addBotMessage(message) {

        const messageElement =
            document.createElement("div");


        messageElement.className =
            "chat-message bot-message";


        messageElement.textContent =
            message;


        chatMessages.appendChild(
            messageElement
        );


        saveMessage(
            "bot",
            message
        );


        scrollToBottom();

    }


    /* =====================================================
       EMERGENCY BUTTON
       ===================================================== */

    function addEmergencyButton() {

        const button =
            document.createElement("a");


        button.href =
            "emergency.html";


        button.className =
            "chat-action emergency-action";


        button.textContent =
            "🚑 Open Emergency SOS";


        chatMessages.appendChild(
            button
        );


        scrollToBottom();

    }


    /* =====================================================
       LINK BUTTON
       ===================================================== */

    function addLinkButton(
        text,
        url
    ) {

        const button =
            document.createElement("a");


        button.href =
            url;


        button.className =
            "chat-action";


        button.textContent =
            text;


        chatMessages.appendChild(
            button
        );


        scrollToBottom();

    }


    /* =====================================================
       TYPING INDICATOR
       ===================================================== */

    function showTypingIndicator() {

        const typing =
            document.createElement("div");


        typing.id =
            "typingIndicator";


        typing.className =
            "chat-message bot-message";


        typing.textContent =
            "ArogyaBandhu is typing...";


        chatMessages.appendChild(
            typing
        );


        scrollToBottom();

    }


    function removeTypingIndicator() {

        const typing =
            document.getElementById(
                "typingIndicator"
            );


        if (typing) {

            typing.remove();

        }

    }


    /* =====================================================
       SAVE CHAT MESSAGE
       ===================================================== */

    function saveMessage(
        sender,
        message
    ) {

        let history =
            JSON.parse(
                localStorage.getItem(
                    STORAGE_KEY
                )
            ) || [];


        history.push({

            sender: sender,

            message: message,

            timestamp:
                new Date().toISOString()

        });


        /*
         * Keep only the latest 100 messages.
         */

        if (history.length > 100) {

            history =
                history.slice(-100);

        }


        localStorage.setItem(
            STORAGE_KEY,
            JSON.stringify(history)
        );

    }


    /* =====================================================
       LOAD CHAT HISTORY
       ===================================================== */

    function loadChatHistory() {

        const history =
            JSON.parse(
                localStorage.getItem(
                    STORAGE_KEY
                )
            ) || [];


        history.forEach(
            function (item) {

                const messageElement =
                    document.createElement("div");


                messageElement.className =
                    item.sender === "user"
                        ? "chat-message user-message"
                        : "chat-message bot-message";


                messageElement.textContent =
                    item.message;


                chatMessages.appendChild(
                    messageElement
                );

            }
        );


        scrollToBottom();

    }


    /* =====================================================
       SCROLL CHAT TO BOTTOM
       ===================================================== */

    function scrollToBottom() {

        chatMessages.scrollTop =
            chatMessages.scrollHeight;

    }

});