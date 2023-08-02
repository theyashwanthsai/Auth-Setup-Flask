from flask import Flask, render_template, request, redirect, url_for, session
import pyrebase
import os
from dotenv import load_dotenv
from functools import wraps

load_dotenv()
app = Flask(__name__, template_folder="templates")
app.secret_key = "your_secret_key"



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# Initialize Firebase configuration
firebase_config = {
    # 'apiKey': "AIzaSyBNHqLuaeZ_k8RWaG4jSh3QwWgZrbnLdX4",
    'apiKey': os.getenv("apiKey"),
    'authDomain': "groovy-scarab-381816.firebaseapp.com",
    'projectId': "groovy-scarab-381816",
    'storageBucket': "groovy-scarab-381816.appspot.com",
    'messagingSenderId': "1092611679235",
    'appId': "1:1092611679235:web:5368cb18b8d232a1721a36",
    'measurementId': "G-Y09T2RDLED",
    'databaseURL': ''
}

firebase = pyrebase.initialize_app(firebase_config)

# Initialize Firebase Authentication
auth = firebase.auth()






@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session["user"] = user
            return redirect(url_for("home"))
        except Exception as e:
            return render_template("login.html", error="Invalid credentials.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = auth.create_user_with_email_and_password(email, password)
            session["user"] = user
            return redirect(url_for("home"))
        except Exception as e:
            return render_template("register.html", error="Registration failed.")
    return render_template("register.html")




@app.route("/verify")
@login_required
def verify():
    return "you are seeing this that means u are authorized!!!"



@app.route("/home")
def home():
    if "user" in session:
        user = session["user"]
        return f"Welcome, {user['email']}! You are logged in."
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, port = 8000)
