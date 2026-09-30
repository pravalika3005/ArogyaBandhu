/* =========================================================
   AROGYABANDHU - APPOINTMENT.JS
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    const appointmentForm = document.getElementById("appointmentForm");

    const doctorSelect = document.getElementById("doctor");
    const dateInput = document.getElementById("appointmentDate");
    const timeSelect = document.getElementById("appointmentTime");
    const consultationType = document.getElementById("consultationType");

    const successMessage = document.getElementById("successMessage");
    const appointmentDetails = document.getElementById("appointmentDetails");


    /* =====================================================
       DOCTOR DATA
       ===================================================== */

    const doctors = {
        general: {
            name: "Dr. Priya Sharma",
            specialization: "General Physician"
        },

        pediatric: {
            name: "Dr. Rahul Kumar",
            specialization: "Pediatrician"
        },

        gynecologist: {
            name: "Dr. Anjali Reddy",
            specialization: "Gynecologist"
        },

        cardiologist: {
            name: "Dr. Arjun Rao",
            specialization: "Cardiologist"
        }
    };


    /* =====================================================
       SET MINIMUM DATE
       Prevent selecting previous dates
       ===================================================== */

    if (dateInput) {

        const today = new Date();

        const year = today.getFullYear();

        const month = String(
            today.getMonth() + 1
        ).padStart(2, "0");

        const day = String(
            today.getDate()
        ).padStart(2, "0");

        dateInput.min = `${year}-${month}-${day}`;
    }


    /* =====================================================
       TIME SLOTS
       ===================================================== */

    const timeSlots = [
        "09:00 AM",
        "10:00 AM",
        "11:00 AM",
        "12:00 PM",
        "02:00 PM",
        "03:00 PM",
        "04:00 PM",
        "05:00 PM"
    ];


    if (timeSelect) {

        timeSelect.innerHTML =
            '<option value="">Select Time</option>';

        timeSlots.forEach(function (time) {

            const option =
                document.createElement("option");

            option.value = time;

            option.textContent = time;

            timeSelect.appendChild(option);

        });
    }


    /* =====================================================
       FORM SUBMISSION
       ===================================================== */

    if (appointmentForm) {

        appointmentForm.addEventListener(
            "submit",
            function (event) {

                event.preventDefault();


                /* -----------------------------------------
                   GET FORM VALUES
                   ----------------------------------------- */

                const patientName =
                    document.getElementById("patientName")?.value.trim();

                const phone =
                    document.getElementById("phone")?.value.trim();

                const doctor =
                    doctorSelect?.value;

                const date =
                    dateInput?.value;

                const time =
                    timeSelect?.value;

                const type =
                    consultationType?.value;


                /* -----------------------------------------
                   VALIDATION
                   ----------------------------------------- */

                if (
                    !patientName ||
                    !phone ||
                    !doctor ||
                    !date ||
                    !time ||
                    !type
                ) {

                    showMessage(
                        "Please fill in all required fields.",
                        "error"
                    );

                    return;
                }


                /* -----------------------------------------
                   PHONE VALIDATION
                   ----------------------------------------- */

                const phonePattern =
                    /^[6-9]\d{9}$/;

                if (!phonePattern.test(phone)) {

                    showMessage(
                        "Please enter a valid 10-digit Indian mobile number.",
                        "error"
                    );

                    return;
                }


                /* -----------------------------------------
                   DOCTOR INFORMATION
                   ----------------------------------------- */

                const selectedDoctor =
                    doctors[doctor];

                if (!selectedDoctor) {

                    showMessage(
                        "Please select a valid doctor.",
                        "error"
                    );

                    return;
                }


                /* -----------------------------------------
                   CREATE APPOINTMENT ID
                   ----------------------------------------- */

                const appointmentId =
                    "AB-" +
                    Date.now()
                        .toString()
                        .slice(-8);


                /* -----------------------------------------
                   APPOINTMENT OBJECT
                   ----------------------------------------- */

                const appointment = {

                    id: appointmentId,

                    patientName: patientName,

                    phone: phone,

                    doctor: selectedDoctor.name,

                    specialization:
                        selectedDoctor.specialization,

                    date: date,

                    time: time,

                    consultationType: type,

                    status: "Confirmed",

                    createdAt:
                        new Date().toISOString()

                };


                /* -----------------------------------------
                   SAVE TO LOCAL STORAGE
                   ----------------------------------------- */

                let appointments =
                    JSON.parse(
                        localStorage.getItem(
                            "arogyaAppointments"
                        )
                    ) || [];


                appointments.push(appointment);


                localStorage.setItem(
                    "arogyaAppointments",
                    JSON.stringify(appointments)
                );


                /* -----------------------------------------
                   SHOW SUCCESS MESSAGE
                   ----------------------------------------- */

                showAppointmentSuccess(
                    appointment
                );


                /* -----------------------------------------
                   RESET FORM
                   ----------------------------------------- */

                appointmentForm.reset();

            }
        );
    }


    /* =====================================================
       DISPLAY SUCCESS MESSAGE
       ===================================================== */

    function showAppointmentSuccess(
        appointment
    ) {

        if (!successMessage) {
            alert(
                "Appointment booked successfully!\n" +
                "Appointment ID: " +
                appointment.id
            );

            return;
        }


        successMessage.style.display =
            "block";

        successMessage.className =
            "success-message";


        if (appointmentDetails) {

            appointmentDetails.innerHTML = `

                <strong>Appointment Confirmed!</strong>

                <p>
                    <b>Appointment ID:</b>
                    ${appointment.id}
                </p>

                <p>
                    <b>Patient:</b>
                    ${appointment.patientName}
                </p>

                <p>
                    <b>Doctor:</b>
                    ${appointment.doctor}
                </p>

                <p>
                    <b>Specialization:</b>
                    ${appointment.specialization}
                </p>

                <p>
                    <b>Date:</b>
                    ${formatDate(appointment.date)}
                </p>

                <p>
                    <b>Time:</b>
                    ${appointment.time}
                </p>

                <p>
                    <b>Consultation:</b>
                    ${appointment.consultationType}
                </p>

                <p>
                    <b>Status:</b>
                    ${appointment.status}
                </p>

            `;
        }


        successMessage.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });
    }


    /* =====================================================
       FORMAT DATE
       ===================================================== */

    function formatDate(date) {

        const dateObject =
            new Date(date + "T00:00:00");

        return dateObject.toLocaleDateString(
            "en-IN",
            {
                day: "2-digit",
                month: "long",
                year: "numeric"
            }
        );
    }


    /* =====================================================
       ERROR / NORMAL MESSAGE
       ===================================================== */

    function showMessage(
        message,
        type
    ) {

        if (!successMessage) {

            alert(message);

            return;
        }


        successMessage.style.display =
            "block";

        successMessage.className =
            type === "error"
                ? "error-message"
                : "success-message";


        if (appointmentDetails) {

            appointmentDetails.innerHTML =
                `<p>${message}</p>`;

        }

    }


    /* =====================================================
       VIEW SAVED APPOINTMENTS
       ===================================================== */

    window.viewAppointments =
        function () {

            const appointments =
                JSON.parse(
                    localStorage.getItem(
                        "arogyaAppointments"
                    )
                ) || [];


            console.log(
                "ArogyaBandhu Appointments:",
                appointments
            );


            return appointments;
        };


    /* =====================================================
       CANCEL APPOINTMENT
       ===================================================== */

    window.cancelAppointment =
        function (appointmentId) {

            let appointments =
                JSON.parse(
                    localStorage.getItem(
                        "arogyaAppointments"
                    )
                ) || [];


            const appointment =
                appointments.find(
                    item =>
                        item.id === appointmentId
                );


            if (!appointment) {

                alert(
                    "Appointment not found."
                );

                return;
            }


            appointment.status =
                "Cancelled";


            localStorage.setItem(
                "arogyaAppointments",
                JSON.stringify(appointments)
            );


            alert(
                "Appointment " +
                appointmentId +
                " has been cancelled."
            );

        };


});