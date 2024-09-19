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

if __name__ == "__main__":
    app.run(port=8000, debug=True)


# Path to the SQLite database file
DATABASE = 'sensors.db'

# Create the database file and table if it doesn’t exist
def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TemperatureReading (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_name TEXT NOT NULL,
                location TEXT NOT NULL,
                temperature REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

# Function to insert a new temperature reading into the database
def save_sensor_data(sensor_name, location, temperature):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO TemperatureReading (sensor_name, location, temperature)
        VALUES (?, ?, ?)
    ''', (sensor_name, location, temperature))
    conn.commit()
    conn.close()

# Function to get the latest 10 temperature readings from the database
def get_latest_readings():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT sensor_name, location, temperature, timestamp
        FROM TemperatureReading
        ORDER BY timestamp DESC
        LIMIT 10
    ''')
    readings = cursor.fetchall()
    conn.close()
    return readings





@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/base/")
def base():
    return render_template("login.html")

@app.route("/dashboard/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/account")
def account():
    return render_template("account.html")

@app.route("/admin_centre/")
def admin_centre():
  #  conn = get_db_connection()
  #  sensors = conn.execute('SELECT * FROM sensors').fetchall()
  #  conn.close()
    return render_template("login.html")

@app.route("/new_sensor", methods=["GET", "POST"])
def new_sensor():
    if request.method == "POST":
        name = request.form.get("name")
        location = request.form.get("location")
        interval = request.form.get("interval")
        
        conn = get_db_connection()
        conn.execute('INSERT INTO sensors (name, location, interval) VALUES (?, ?, ?)',
                     (name, location, interval))
        conn.commit()
        conn.close()
        
        return redirect(url_for('admin_centre'))
    
        print("inserting into table ", + name + ' ' + location + ' ' + interval)
    
    return render_template("new_sensor.html")



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
        

    return render_template("admin_centre.html")


# Simulating temperature data from various sensors
SENSORS = {
    "sensor_1": {"location": "office", "temp": 0},
    "sensor_2": {"location": "server_room_1", "temp": 0},
    "sensor_3": {"location": "server_room_2", "temp": 0},
    "sensor_4": {"location": "Storage_room", "temp": 0},
}



# Function to simulate and save temperature readings
def get_and_save_sensor_data():
    for sensor, data in SENSORS.items():
        temperature = round(random.uniform(20.0, 30.0), 2)
        SENSORS[sensor]["temp"] = temperature
        # Save the data to the SQLite database
        save_sensor_data(sensor, data["location"], temperature)
    return SENSORS

# Initialize the database
init_db()


@app.route('/api/sensor-data')
def sensor_data():
    sensor_data = get_and_save_sensor_data()
    return jsonify(sensor_data)


@app.route('/readings')
def readings():
    latest_readings = get_latest_readings()  # Fetch the latest readings from the database
    return render_template('readings.html', readings=latest_readings) 



if __name__ == "__main__":
    app.run(debug=True)