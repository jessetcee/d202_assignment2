import time
import json
import random
import sqlite3
import requests
import requests.exceptions

from datetime import datetime

url = 'http://127.0.0.1:5000/add_reading'

def send_meter_data():
    conn = sqlite3.connect('../database.db')
    while True:
        data = []
        sensors = conn.execute("SELECT * FROM Sensor")
        # sensors = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        
        for sensor in sensors.fetchall():
            reading = 0
            
            if sensor[4] == "ACTIVE":
                reading = random.randint(20, 35)

            data.append({
                "id": sensor[0],
                "location": sensor[2],
                "description": sensor[3],
                "reading": reading,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        json_data = json.dumps(data)

        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, data=json_data, headers=headers)
            print(f"Data sent: {data}, Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')

        time.sleep(5)

def add_col_to_table():
    conn = sqlite3.connect("../database.db")
    # conn.execute("ALTER TABLE Sensor ADD COLUMN area VARCHAR(255)")
    # conn.execute("ALTER TABLE Sensor ADD COLUMN description VARCHAR(255)")
    # conn.execute("ALTER TABLE Sensor ADD COLUMN status VARCHAR(8)")

    # conn.execute("ALTER TABLE TemperatureReading ADD COLUMN location VARCHAR(255)")
    # conn.execute("ALTER TABLE TemperatureReading DROP COLUMN area")

    # conn.execute("ALTER TABLE Sensor DROP COLUMN area")

    print(conn.execute("SELECT * FROM Sensor").fetchall())

def get_sql_data():
    conn = sqlite3.connect("../database.db")
    data = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")

    for table in data:
        table_name = table[0]
        table_info = conn.execute("SELECT * FROM " + table_name)
        print(table_name)
        # print(table_info.description)
        for column_header in table_info.description:
            print(f'col: {column_header[0]}|')

    # print(conn.execute("SELECT * FROM Sensor").fetchall())

def change_sensor_info():
    conn = sqlite3.connect("../database.db")
    cursor = conn.cursor()
    
    sensors = cursor.execute("SELECT * FROM Sensor").fetchall()
    conn.commit()

    for sensor in sensors:
        longitude = random.uniform(-180, 180)
        latitude = random.uniform(-90, 90)
        location = f'{longitude:.3f}, {latitude:.3f}'

        status = "ACTIVE"

        description = "N/A"

        query = f"UPDATE Sensor SET location = '{location}', status = '{status}', description = '{description}' WHERE id = + {str(sensor[0])}"
        
        cursor.execute(query)
        conn.commit()
    
    conn.close()

# change_sensor_info()
# add_col_to_table()
# get_sql_data()
send_meter_data()