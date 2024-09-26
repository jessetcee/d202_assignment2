function updateSensorData() {
    console.log('refresh');
    location.reload();
}

// Update sensor data every 5 seconds
setInterval(updateSensorData, 4000);

// Fetch initial sensor data when the page loads
updateSensorData();
