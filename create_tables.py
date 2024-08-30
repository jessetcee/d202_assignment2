import sqlite3

conn = sqlite3.connect('database.db')
print("Connected to database successfully")

# Create SENSOR table
conn.execute('''
    CREATE TABLE sensors (
        sensor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        interval INT NOT NULL
    )
''')
print("Created sensors table successfully!")

# Create TEMPERATURE_READING table
conn.execute('''
    CREATE TABLE temp_readings (
        reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sensor_id INTEGER NOT NULL,
        temperature FLOAT NOT NULL,
        timestamp DATETIME NOT NULL,
        FOREIGN KEY (sensor_id) REFERENCES sensors (sensor_id)
    )
''')
print("Created temp_readings table successfully!")

conn.close()