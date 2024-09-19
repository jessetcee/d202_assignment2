import datetime
import sqlite3
import random
import time
import os
import sqlite3
from flask import render_template, Flask, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'super_secret_key'
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# Path to the SQLite database file
DATABASE = 'sensors.db'

# Create the database file and table if it doesn’t exist
def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

    #Create Sensor table    
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Sensor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_name TEXT NOT NULL,
            location TEXT NOT NULL
        )
    ''')

# Create TemperatureReading table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TemperatureReading (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id INTEGER,
            
            temperature REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sensor_id) REFERENCES Sensor(id)
        )
    ''')

        conn.commit()
        conn.close()


# Function to add a new sensor to the database
def add_sensor(sensor_name, location):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Sensor (sensor_name, location)
        VALUES (?, ?)
    ''', (sensor_name, location))
    conn.commit()
    conn.close()


# Function to get all sensors from the database
def get_all_sensors():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, sensor_name, location FROM Sensor')
    sensors = cursor.fetchall()
    conn.close()
    return sensors

# Function to insert a new sensor into the database
def save_sensor_data(sensor_id, temperature):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO TemperatureReading (sensor_id, temperature)
        VALUES (?, ?)
    ''', (sensor_id, temperature))
    conn.commit()
    conn.close()

# Function to get the latest 10 temperature readings from the database
def get_latest_readings():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT distinct s.id, s.sensor_name, s.location, r.temperature, r.timestamp
        FROM TemperatureReading r
        JOIN Sensor s ON r.sensor_id = s.id
        ORDER BY r.timestamp DESC
        LIMIT 10
    ''')
    readings = cursor.fetchall()
    conn.close()
    return readings

#readings for dashboard
def get_live_readings():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT distinct s.sensor_name, s.location, r.temperature, r.timestamp
        FROM TemperatureReading r
        JOIN Sensor s ON r.sensor_id = s.id
        ORDER BY r.timestamp DESC
        LIMIT 25
    ''')
    readings = cursor.fetchall()
    conn.close()
    return readings

# Function to simulate and save temperature readings
def get_and_save_sensor_data():
    sensors = get_all_sensors()  # Get all sensors from the database
    for sensor in sensors:
        sensor_id, sensor_name, location = sensor
        temperature = round(random.uniform(20.0, 30.0), 2)
        save_sensor_data(sensor_id, temperature)  # Save the temperature reading for the sensor
    # return sensors

# Initialize the database
init_db()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard/")
def dashboard():
    get_and_save_sensor_data()
    latest_readings = get_latest_readings()
    return render_template("dashboard.html", readings=latest_readings)

@app.route("/admin_centre/")
def admin_centre():
    conn = get_db_connection()
    sensors = conn.execute('SELECT * FROM TemperatureReading').fetchall()
    conn.close()
    return render_template("admin_centre.html")
# , sensors=sensors

# @app.route("/new_sensor", methods=["GET", "POST"])
# def new_sensor():
#     if request.method == "POST":
#         name = request.form.get("name")
#         location = request.form.get("location")
#         interval = request.form.get("interval")
        
#         conn = get_db_connection()
#         conn.execute('INSERT INTO sensors (name, location, interval) VALUES (?, ?, ?)',
#                      (name, location, interval))
#         conn.commit()
#         conn.close()
        
#         return redirect(url_for('admin_centre'))
    
#     return render_template("readings.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                       (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            session['is_admin'] = user['is_admin']  # Store the admin status in the session
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials, please try again."

    return render_template("login.html")





@app.route('/api/sensor-data')
def sensor_data():
    sensor_data = get_and_save_sensor_data()
    return jsonify(sensor_data)



@app.route('/readings')
def readings():
    latest_readings = get_latest_readings()  # Fetch the latest readings from the database
    return render_template('readings.html', readings=latest_readings) 

@app.route('/add-sensor', methods=['GET', 'POST'])
def add_sensor_route():
    if request.method == 'POST':
        sensor_name = request.form['sensor_name']
        location = request.form['location']
        add_sensor(sensor_name, location)  # Add sensor to the database
        return redirect(url_for('readings'))  # Redirect back to the readings page
    
    return render_template('add_sensor.html')  # Render the form to add a new sensor


# Testing code, currently errors
def delete_temp_readings():
    conn= sqlite3.connect(DATABASE)
    cursor= conn.cursor()
    cursor.execute('delete from TemperatureReading')
    conn.commit
    conn.close
    return redirect(url_for('readings'))

if __name__ == "__main__":
    app.run(debug=True)


