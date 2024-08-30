import sqlite3

# Connect to the existing database
conn = sqlite3.connect('database.db')
print("Connected to database successfully")

# Create a cursor object
cursor = conn.cursor()

# Insert an admin user
try:
    cursor.execute('''
        INSERT INTO users (username, password, is_admin)
        VALUES (?, ?, ?)
    ''', ('admin', 'password', True))
    print("Admin user created successfully!")
except sqlite3.IntegrityError:
    print("Admin user already exists!")

# Insert a standard user
try:
    cursor.execute('''
        INSERT INTO users (username, password, is_admin)
        VALUES (?, ?, ?)
    ''', ('user', 'password', False))
    print("Standard user created successfully!")
except sqlite3.IntegrityError:
    print("Standard user already exists!")

# Commit the changes and close the connection
conn.commit()
conn.close()