from app import get_all_sensors
import random, json, requests, time

url = 'http://127.0.0.1:5000/api/sensor-data'

# Function to simulate and save temperature readings
# def get_and_save_sensor_data():
#     while True: 
#         sensors = get_all_sensors()  # Get all sensors from the database
#         for sensor in sensors:
#             sensor_id, sensor_name, location = sensor
#             temperature = round(random.uniform(20.0, 30.0), 2)
#             data = {
#                 "id": sensor_id,
#                 "name": sensor_name,
#                 "location": location,
#                 "temperature": temperature  # simulate temperature
#             }
#             json_data = json.dumps(data)
#             try:
#                 # POST request with the JSON data
#                 headers = {'Content-Type': 'application/json'}
#                 response = requests.post(url, json=data, headers=headers)
#             except Exception as e:
#                 print(f"Error: {e}")
#             time.sleep(4)
        
# if __name__ == "__main__":
#     get_and_save_sensor_data()


# Keep track of when each sensor's data was last inserted
last_inserted_data = {}

# Function to simulate and update temperature readings
def get_and_update_sensor_data():
    while True:
        sensors = get_all_sensors()  # Get all sensors from the database
        for sensor in sensors:
            sensor_id, sensor_name, location = sensor
            temperature = round(random.uniform(20.0, 30.0), 2)

            # Prepare the data to be sent
            data = {
                "id": sensor_id,
                "name": sensor_name,
                "location": location,
                "temperature": temperature  # Simulate temperature
            }
            json_data = json.dumps(data)

            try:
                # Send an update request to the server
                headers = {'Content-Type': 'application/json'}
                response = requests.put(url, json=data, headers=headers)  # Use PUT method for update

                if response.status_code == 200:  # Successful update
                    print(f"Data updated for sensor {sensor_name}: {data}, Status Code: {response.status_code}")
                else:
                    print(f"Failed to update data for sensor {sensor_name}: {response.status_code}")

            except Exception as e:
                print(f"Error: {e}")

        # Sleep for 30 seconds before next update cycle
        time.sleep(4)

if __name__ == "__main__": 
    get_and_update_sensor_data()