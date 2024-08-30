import datetime
import sqlite3
from flask import render_template, Flask, request, redirect, url_for

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/admin_centre/")
def admin_centre():
    return render_template("admin_centre.html")

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name="results"):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.datetime.now()
    )

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
            return f"Logged in as {username}"
        else:
            return "Invalid credentials, please try again."

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)