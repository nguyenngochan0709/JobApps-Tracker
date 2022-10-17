# Python code for web server
import os
import pytz
import json

from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

STATUS = [
    "Submitted",
    "In Progress",
    "Rejected",
    "Successful"
]

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///applications.db")

# timezone object containing current timezone
timezone = pytz.timezone("Asia/Singapore")
# datetime object containing current date and time
now = datetime.now(tz=timezone)
# Format the object to dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show an interactive table of job applications submitted"""
    return render_template("index.html")


@app.route("/history")
@login_required
def history():
    """Show a list of job applications previously submitted"""
    history = db.execute("SELECT * FROM applications_tracker WHERE user_id = ?", session.get("user_id"))
    if len(history) == 0:
        return apology("No applications submitted", 403)
    return render_template("history.html", history=history)

@app.route("/ProcessNewContent/<string:content_request>", methods=["POST"])
@login_required
def ProcessNewContent(content_request):
    content_lst = json.loads(content_request)
    value_id = content_lst[0]
    col_id = content_lst[1]
    curr_content = content_lst[2]
    new_content = content_lst[3]
    if col_id == "job_title":
        db.execute("UPDATE applications_tracker SET job_title = ? WHERE user_id = ? AND value_id = ?", new_content, session.get("user_id"), value_id)
    elif col_id == "company":
        db.execute("UPDATE applications_tracker SET company = ? WHERE user_id = ? AND value_id = ?", new_content, session.get("user_id"), value_id)
    elif col_id == "job_id":
        db.execute("UPDATE applications_tracker SET job_id = ? WHERE user_id = ? AND value_id = ?", new_content, session.get("user_id"), value_id)
    elif col_id == "application_date":
        db.execute("UPDATE applications_tracker SET application_date = ? WHERE user_id = ? AND value_id = ?", new_content, session.get("user_id"), value_id)
    elif col_id == "application_status":
        db.execute("UPDATE applications_tracker SET application_status = ? WHERE user_id = ? AND value_id = ?", new_content, session.get("user_id"), value_id)
    elif col_id == "remarks":
        db.execute("UPDATE applications_tracker SET remarks = ? WHERE user_id = ? AND value_id = ?", new_content, session.get("user_id"), value_id)
    elif col_id == "url":
        db.execute("UPDATE applications_tracker SET url = ? WHERE user_id = ? AND value_id = ?", new_content, session.get("user_id"), value_id)
    # db.execute("UPDATE applications_tracker SET ??? = ? WHERE user_id = ?", ???, new_content, session.get("user_id"))
    print(f"Row to be updated: {value_id}")
    print(f"Column to be updated: {col_id}")
    print(f"Current content to be updated: {curr_content}")
    print(f"New content: {new_content}")
    return("/")


@app.route("/entry", methods=["GET", "POST"])
@login_required
def entry():
    """Allow user to create entries for job applications to be tracked"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # If user's input is blank in any of the 3 required fields (job title, company, job id), return an apology
        if not request.form.get("job_title"):
            return apology("Kindly provide a job title", 400)
        if not request.form.get("company"):
            return apology("Kindly provide a company name", 400)
        if not request.form.get("job_id"):
            return apology("Kindly provide a job id", 400)
        if not request.form.get("application_date"):
            return apology("Kindly provide an application date", 400)
        if not request.form.get("application_status"):
            return apology("Kindly provide an application status", 400)
        if not request.form.get("remarks"):
            return apology("Kindly provide remarks", 400)
        if not request.form.get("url"):
            return apology("Kindly provide an URL", 400)
        # Add the new entry to database for record
        curr_valCount = db.execute("SELECT MAX(value_id) FROM applications_tracker WHERE user_id = ?", session.get("user_id"))
        new_valCount = int(curr_valCount[0]["MAX(value_id)"]) + 1
        print(type(new_valCount))
        db.execute("INSERT INTO applications_tracker (user_id, job_title, company, job_id, application_date, application_status, remarks, url, value_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", session.get("user_id"), request.form.get("job_title"), request.form.get("company"), request.form.get("job_id"), request.form.get("application_date"), request.form.get("application_status"), request.form.get("remarks"), request.form.get("url"), new_valCount)
        return redirect("/history")
        # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("entry.html", status=STATUS)

@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    """Display charts about the job applications done"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # If user's input is blank in any of the 3 required fields (job title, company, job id), return an apology
        return redirect("/history")
        # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("home.html", status=STATUS)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/history")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Require a user to input a username
        username = request.form.get("username")
        # If user's input is blank or the username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if not request.form.get("username") or len(rows) != 0:
            return apology("Must provide a username", 400)
        # Require a user to input a password
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # If either input is blank or the passwords do not match
        if not request.form.get("password") or not request.form.get("confirmation") or password != confirmation:
            return apology("Must provide a password", 400)
        # Insert the new user into users
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))
        # Redirect user to home page
        return redirect("/", 200)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Submit the user's input to /register
        return render_template("register.html")