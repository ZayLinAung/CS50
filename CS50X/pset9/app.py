import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    data = db.execute("SELECT symbol, name, SUM(shares), price FROM record WHERE user_id=? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
    return render_template("index.html", data=data, cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not symbol:
            return apology("Missing symbol")
        if not shares:
            return apology("Missing shares")
        if not shares.isdigit():
            return apology("Invalid Symbol")
        quote = lookup(symbol)
        if quote == None:
            return apology("Symbol not found")
        user_cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
        if user_cash[0]["cash"] < quote["price"]:
            return apology("Not enough cash")
        else:
            current_time = datetime.datetime.now()
            amount = quote["price"] * float(shares)
            username = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])
            db.execute("INSERT INTO record(timestramp, user_id, username, status, symbol, name, shares, price) VALUES(?,?,?,?,?,?,?,?)", current_time,session["user_id"], username[0]["username"], "buy", symbol, quote["name"], shares, quote["price"])
            final_cash = user_cash[0]["cash"] - amount
            db.execute("UPDATE users SET cash= ? WHERE id= ?", final_cash, session["user_id"])

            return redirect("/")
    else:
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("SELECT symbol, shares, price, timestramp FROM record WHERE user_id=?", session["user_id"])
    return render_template("history.html", history=history)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        if quote == None:
            return apology("Symbol not found")
        else:
            return render_template("quoted.html", quote=quote)
    else:
        return render_template("quote.html")

    return apology("TODO")


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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not symbol:
            return apology("Missing Symbol")
        if not shares:
            return apology("Missing Shares")
        shares_own= db.execute("SELECT SUM(shares) FROM record WHERE user_id=? AND symbol=?", session["user_id"], symbol)
        if shares_own[0]["SUM(shares)"] < int(shares):
            return apology("Not enough shares owned")
        quote = lookup(symbol)
        current_time = datetime.datetime.now()
        username = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])
        db.execute("INSERT INTO record(timestramp, user_id, username, status, symbol, name, shares, price) VALUES(?,?,?,?,?,?,?,?)", current_time,session["user_id"], username[0]["username"],"sell",symbol, quote["name"],-abs(int(shares)),quote["price"])
        user_cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
        cash_left = user_cash[0]["cash"] + (quote["price"] * float(shares))
        db.execute("UPDATE users SET cash=? WHERE id=?", cash_left, session["user_id"])

        return redirect("/")

    else:
        symbols = db.execute("SELECT symbol FROM record WHERE user_id=? GROUP BY symbol", session["user_id"])
        return render_template("sell.html", symbols=symbols)

@app.route("/myaccount", methods=["GET", "POST"])
@login_required
def myaccount():
    if request.method == "POST":
        username = request.form.get("username")
        orgpassword = request.form.get("originalpassword")
        newpassword = request.form.get("newpassword")
        cash = request.form.get("cash")

        if username:
            db.execute("UPDATE users SET username=? WHERE id=?", username, session["user_id"])
            db.execute("UPDATE record SET username=? WHERE user_id=?", username, session["user_id"])
        if (orgpassword and not newpassword) or (newpassword and not orgpassword):
            return apology("Please fill in both fields to change password")
        if orgpassword and newpassword:
            rows = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])
            if not check_password_hash(rows[0]["hash"], orgpassword):
                return apology("INVALID PASSWORD")
            db.execute("UPDATE users SET hash=? WHERE id=?", generate_password_hash(newpassword, method='pbkdf2:sha256', salt_length=8), session["user_id"])

        if cash:
            currentcash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
            newcash=currentcash[0]["cash"] + float(cash)
            db.execute("UPDATE users SET cash=? WHERE id=?", newcash, session["user_id"] )

        return redirect("/myaccount")
    else:
        profile = db.execute("SELECT username, cash FROM users WHERE id=?", session["user_id"])
        stocks = db.execute("SELECT symbol FROM record WHERE user_id=? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])
        return render_template("myaccount.html", profile=profile, stocks=stocks)

@app.route("/edit")
@login_required
def edit():
    return render_template("edit.html")

@app.route("/deleteacc")
@login_required
def delete():
    db.execute("DELETE FROM record WHERE user_id=?", session["user_id"])
    db.execute("DELETE FROM users WHERE id=?", session["user_id"])
    session.clear()

    return redirect ("/login")
