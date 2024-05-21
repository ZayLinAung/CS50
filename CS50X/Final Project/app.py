import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

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
    """Show portfolio of stocks"""
    data = db.execute("SELECT * FROM posts")
    return render_template("index.html", data=data)


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
        return redirect("/")

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
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username")

        if not password or not confirmation:
            return apology("must provide password")

        if password != confirmation:
            return apology("confirm your password again")

        database = db.execute("SELECT username FROM users WHERE username=?", username)
        if (len(database) != 0):
            return apology("username already exists", 400)

        db.execute("INSERT INTO users(username,hash) VALUES (?,?)", username, generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))
        id = db.execute("SELECT id FROM users WHERE username=?", username)
        session["user_id"] = id[0]["id"]
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        if not title:
            return apology("must provide title")

        if not content:
            return apology("must provide content")

        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        db.execute("INSERT INTO posts(timestramp, user_id, username, title, content) VALUES (?,?,?,?,?)", datetime.datetime.now(), session["user_id"], username[0]["username"], title, content)
        return redirect("/")

    else:
        return render_template("createpost.html")

@app.route("/reply", methods=["GET", "POST"])
def reply():
    if request.method == "POST":
        id = request.form.get("id")
        orgpost = db.execute("SELECT * FROM posts WHERE id=?", id)
        replies = db.execute ("SELECT * FROM replies WHERE originalPost_id=?", id)
        return render_template("replymessage.html", orgpost = orgpost, replies = replies, currentID = session["user_id"])

@app.route("/viewreply", methods=["GET", "POST"])
def viewreply():
    if request.method == "POST":
        replycontent = request.form.get("content")
        orgid = request.form.get("orgid")
        orgpost = db.execute("SELECT * FROM posts WHERE id=?", orgid)
        username = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])
        db.execute("INSERT INTO replies(originalPost_id, timestramp, user_id, username, content) VALUES (?,?,?,?,?)", orgid, datetime.datetime.now(), session["user_id"], username[0]["username"], replycontent)
        replies = db.execute ("SELECT * FROM replies WHERE originalPost_id=?", orgid)
        return render_template("viewreply.html", orgpost = orgpost, replies = replies, currentID = session["user_id"])

@app.route("/mypost")
@login_required
def mypost():
    posts = db.execute("SELECT * FROM posts WHERE user_id=?", session["user_id"])
    return render_template("index.html", data = posts)