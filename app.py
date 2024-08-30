import re
from datetime import datetime
from flask import render_template, Flask, request, redirect, url_for

app = Flask(__name__)

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
        date=datetime.now()
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Handle the login logic here (authentication, etc.)
        return f"Logged in as {username}"
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)