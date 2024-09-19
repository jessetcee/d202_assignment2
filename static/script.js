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
// Fetch sensor data from Flask API
async function fetchSensorData() {
    const response = await fetch('/api/sensor-data');
    const data = await response.json();

    // Update the HTML for each sensor
    document.getElementById('sensor_1_temp').innerText = data.sensor_1.temp + "°C";
    document.getElementById('sensor_2_temp').innerText = data.sensor_2.temp + "°C";
    document.getElementById('sensor_3_temp').innerText = data.sensor_3.temp + "°C";
    document.getElementById('sensor_4_temp').innerText = data.sensor_4.temp + "°C";

    // Update the graph
    updateGraph([data.sensor_1.temp, data.sensor_2.temp, data.sensor_3.temp, data.sensor_4.temp]);
}

// Initialize the graph using Chart.js
function initGraph() {
    const ctx = document.getElementById('sensorChart').getContext('2d');
    window.sensorChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Office', 'Server Room 1', 'Server Room 2', 'Storage Room'],
            datasets: [{
                label: 'Temperature (°C)',
                data: [0, 0, 0, 0],  // Initial dummy data
                backgroundColor: ['#3498db', '#2ecc71', '#e74c3c', '#9b59b6'],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    suggestedMax: 50
                }
            }
        }
    });
}

// Update the graph with new sensor data
function updateGraph(sensorData) {
    window.sensorChart.data.datasets[0].data = sensorData;
    window.sensorChart.update();
}

// Fetch data and initialize graph on page load
window.onload = function() {
    initGraph();
    fetchSensorData();

    // Optionally, refresh the data every 10 seconds
    setInterval(fetchSensorData, 10000);
};
