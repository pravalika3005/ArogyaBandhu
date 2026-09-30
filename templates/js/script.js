// emergency.js

document.addEventListener("DOMContentLoaded", function () {

    const sosButton = document.getElementById("sosButton");
    const statusMessage = document.getElementById("statusMessage");
    const locationText = document.getElementById("locationText");

    if (sosButton) {
        sosButton.addEventListener("click", function () {
            activateEmergency();
        });
    }

    function activateEmergency() {

        const confirmSOS = confirm(
            "Are you sure you want to activate Emergency SOS?\n\n" +
            "Your emergency contacts and ASHA worker will be notified."
        );

        if (!confirmSOS) {
            return;
        }

        updateStatus("Activating Emergency SOS...");

        // Get user's GPS location
        if (navigator.geolocation) {

            navigator.geolocation.getCurrentPosition(
                function (position) {

                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;

                    const location = {
                        latitude: latitude,
                        longitude: longitude,
                        timestamp: new Date().toISOString()
                    };

                    console.log("Emergency Location:", location);

                    displayLocation(latitude, longitude);

                    sendEmergencyAlert(location);
                },

                function (error) {

                    console.error("Location Error:", error);

                    updateStatus(
                        "Unable to access GPS location. Emergency alert will continue without location."
                    );

                    sendEmergencyAlert(null);
                },

                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 0
                }
            );

        } else {

            updateStatus(
                "GPS is not supported by this browser."
            );

            sendEmergencyAlert(null);
        }
    }


    function sendEmergencyAlert(location) {

        updateStatus("Sending emergency alerts...");

        /*
         * DEMO MODE
         *
         * In the real application this section should send
         * the emergency request to your backend.
         *
         * Example:
         *
         * fetch("/api/emergency", {
         *     method: "POST",
         *     headers: {
         *         "Content-Type": "application/json"
         *     },
         *     body: JSON.stringify({
         *         patientId: "PATIENT_ID",
         *         location: location
         *     })
         * });
         */

        setTimeout(function () {

            updateStatus(
                "Emergency alert sent successfully."
            );

            showEmergencyContacts();

        }, 1500);
    }


    function displayLocation(latitude, longitude) {

        if (locationText) {

            locationText.innerHTML =
                "📍 Location detected<br>" +
                "Latitude: " + latitude.toFixed(6) + "<br>" +
                "Longitude: " + longitude.toFixed(6);

        }
    }


    function showEmergencyContacts() {

        const alertBox = document.createElement("div");

        alertBox.className = "emergency-success";

        alertBox.innerHTML = `
            <h3>🚑 Emergency SOS Activated</h3>

            <p>Notifications sent to:</p>

            <ul>
                <li>👨‍👩‍👧 Emergency Contact</li>
                <li>👩‍⚕️ ASHA Worker</li>
                <li>🏥 Nearby Healthcare Center</li>
                <li>🚑 Emergency Service</li>
            </ul>

            <p>
                Please stay calm and remain at your current location
                if it is safe to do so.
            </p>
        `;

        document.body.appendChild(alertBox);

        setTimeout(function () {
            alertBox.remove();
        }, 8000);
    }


    function updateStatus(message) {

        if (statusMessage) {
            statusMessage.textContent = message;
        }

        console.log(message);
    }

});