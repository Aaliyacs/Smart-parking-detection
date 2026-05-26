// ------------------------------------
// FETCH PARKING DATA FROM FLASK API
// ------------------------------------
async function fetchParkingData() {

    try {

        // API Request
        const response = await fetch(
            "http://127.0.0.1:5000/parking-data"
        );

        // Convert response to JSON
        const data = await response.json();

        // ------------------------------------
        // UPDATE DASHBOARD STATS
        // ------------------------------------
        document.getElementById("total-slots").textContent =
            data.total || 0;

        document.getElementById("occupied-slots").textContent =
            data.occupied || 0;

        document.getElementById("available-slots").textContent =
            data.available || 0;

        document.getElementById("occupancy").textContent =
            (data.occupancy || 0) + "%";

        // ------------------------------------
        // UPDATE PAGE TITLE DYNAMICALLY
        // ------------------------------------
        document.title =
            `Parking Occupancy: ${data.occupancy || 0}%`;

        // ------------------------------------
        // UPDATE STATUS COLOR BASED ON OCCUPANCY
        // ------------------------------------
        const occupancyElement =
            document.getElementById("occupancy");

        const occupancyValue = data.occupancy || 0;

        // LOW OCCUPANCY
        if (occupancyValue < 50) {

            occupancyElement.style.color = "#22c55e";

        }

        // MEDIUM OCCUPANCY
        else if (occupancyValue >= 50 &&
                 occupancyValue < 80) {

            occupancyElement.style.color = "#facc15";

        }

        // HIGH OCCUPANCY
        else {

            occupancyElement.style.color = "#ef4444";

        }

        // ------------------------------------
        // CONSOLE LOG (OPTIONAL)
        // ------------------------------------
        console.clear();

        console.log("Smart Parking Data");
        console.log("-------------------");

        console.log(
            "Total Slots:",
            data.total
        );

        console.log(
            "Occupied Slots:",
            data.occupied
        );

        console.log(
            "Available Slots:",
            data.available
        );

        console.log(
            "Occupancy:",
            data.occupancy + "%"
        );

    }

    // ------------------------------------
    // ERROR HANDLING
    // ------------------------------------
    catch (error) {

        console.log(
            "API Error:",
            error
        );

        // Show fallback values
        document.getElementById("total-slots").textContent = "0";

        document.getElementById("occupied-slots").textContent = "0";

        document.getElementById("available-slots").textContent = "0";

        document.getElementById("occupancy").textContent = "Offline";

    }
}

// ------------------------------------
// INITIAL LOAD
// ------------------------------------
fetchParkingData();

// ------------------------------------
// AUTO REFRESH EVERY 1.5 SECONDS
// ------------------------------------
setInterval(fetchParkingData, 1500);