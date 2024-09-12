function updateSensorData() {
    fetch('/api/sensor-data')
        .then(response => response.json())
        .then(data => {
            for (const sensor in data) {
                document.getElementById(`${sensor}_temp`).innerText = data[sensor].temp;
            }
        });
}

// Update sensor data every 5 seconds
setInterval(updateSensorData, 5000);

// Fetch initial sensor data when the page loads
updateSensorData();
