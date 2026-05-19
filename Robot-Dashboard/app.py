from flask import Flask, render_template, request, redirect, session, flash
from functools import wraps
from robot_api import get_status, move_robot
from database import log_command, get_logs, create_user, get_user
from database import init_db
init_db()

app = Flask(__name__)
app.secret_key = "change_this_in_production"


# ------------------ AUTH DECORATOR ------------------
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper


# ------------------ REGISTER ------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")

        if not username or not password:
            flash("All fields required")
            return redirect("/register")

        if get_user(username):
            flash("User already exists")
            return redirect("/register")

        create_user(username, password, role)
        flash("Registration successful")
        return redirect("/login")

    return render_template("register.html")


# ------------------ LOGIN ------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = get_user(username)

        if not user or user["password"] != password:
            flash("Invalid credentials")
            return redirect("/login")

        session["user"] = username
        session["role"] = user["role"]

        return redirect("/")

    return render_template("login.html")


# ------------------ LOGOUT ------------------
@app.route("/logout")
def logout():
    session.clear()
    flash("You have successfully logged out.")
    return redirect("/login")


# ------------------ HOME ------------------
@app.route("/")
@login_required
def index():
    status = get_status()

    # 🔥 FIX 1: Ensure status is always a dictionary
    if not status or not isinstance(status, dict):
        status = {}

    # 🔥 FIX 2: Handle offline case safely
    if status.get("status") == "offline":
        status["online"] = False
        status["battery"] = "N/A"
        status["position"] = {"x": "-", "y": "-"}
        status["message"] = "Reconnecting..."
    else:
        status["online"] = True
        status["message"] = "System Online"

    # 🔥 FIX 3: Ensure position always exists
    if "position" not in status or not isinstance(status["position"], dict):
        status["position"] = {"x": 0, "y": 0}

    logs = get_logs()

    return render_template("index.html", status=status, logs=logs)


# ------------------ MOVE ------------------
@app.route("/move", methods=["POST"])
@login_required
def move():
    if session.get("role") != "commander":
        flash("Access Denied: You don't have the right permissions.")
        return redirect("/")

    direction = request.form.get("direction")

    if direction not in ["up", "down", "left", "right"]:
        flash("Invalid direction. Please choose 'up', 'down', 'left', or 'right'.")
        return redirect("/")

    try:
        move_robot(direction)  # movement handled in robot_api
        log_command(session.get("user"), direction)
        flash(f"Robot moved {direction}.")
    except Exception as e:
        flash(f"Error while moving robot: {str(e)}")

    return redirect("/")


# ------------------ RUN ------------------
if __name__ == "__main__":
    app.run(debug=True)