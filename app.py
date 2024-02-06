import os
import datetime
import pytz
import random

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology, translate, cards

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///flashcards.db")

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

    # Recall user's id
    user_id = session["user_id"]

    # modify database list
    reg_list = db.execute(
        "SELECT source, target, datetime FROM database WHERE user_id = ? GROUP BY source", user_id)

    print(reg_list)

    '''# Update reg_list and calculate stock value
    for row in reg_list:
        row["price"] = lookup(row["symbol"])["price"]
        stock_value = stock_value + (row["price"] * row["shares"])

    # Calculate remaining cash
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    # Calculate overall value of the assets
    total = stock_value + cash'''

    return render_template("index.html", reg_list=reg_list)


@app.route("/process", methods=["POST"])
def process():
    data = request.form.get('data')
    # process the data using Python code
    result = translate(data)
    return result

@app.route("/add", methods=["GET", "POST"])
def add():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Assign values
        word_1 = request.form.get("word_1")
        word_2 = request.form.get("word_2")
        word_3 = request.form.get("word_3")
        word_4 = request.form.get("word_4")
        translation_1 = request.form.get("translation_1")
        translation_2 = request.form.get("translation_2")
        translation_3 = request.form.get("translation_3")
        translation_4 = request.form.get("translation_4")

        # Number of flashcards added
        x = 1

        # Check if at least one word added
        if not word_1:
            return apology("add at least first word")

        # Check if at least one translation added
        elif not translation_1:
            return apology("add at least first translation")

        # Check if there is translation for given word
        if word_2 and not translation_2 or word_3 and not translation_3 or word_4 and not translation_4:
            return apology("missing translation")

        # Check if there is word for given translation
        if translation_2 and not word_2 or translation_3 and not word_3 or translation_4 and not word_4:
            return apology("missing word")

        # Check how many flashcards user wants to add
        if word_2:
            x = 2
        if word_3:
            x = 3
        if word_4:
            x = 4

        # Recall user's id
        user_id = session["user_id"]

        # Check user's amount of credits
        funds = db.execute("SELECT credits FROM users WHERE id = ?", user_id)[0]["credits"]

        # Check time and date
        date_time = datetime.datetime.now(pytz.timezone("Europe/Warsaw"))

        # Check if user has enough money to buy the stock
        if funds < x:
            return apology("not enough credit")

        # Calculate remaining funds
        remaining_credit = funds - x

        # Update 'cash' field in users
        db.execute("UPDATE users SET credits = ? WHERE id = ?", remaining_credit, user_id)

        # Update transactions table
        if x == 1:
            db.execute("INSERT INTO database (user_id, source, target, datetime) VALUES (?, ?, ?, ?)",
                   user_id, word_1, translation_1, date_time)
        if x == 2:
            db.execute("INSERT INTO database (user_id, source, target, datetime) VALUES (?, ?, ?, ?)",
                   user_id, word_1, translation_1, date_time)
            db.execute("INSERT INTO database (user_id, source, target, datetime) VALUES (?, ?, ?, ?)",
                   user_id, word_2, translation_2, date_time)
        if x == 3:
            db.execute("INSERT INTO database (user_id, source, target, datetime) VALUES (?, ?, ?, ?)",
                   user_id, word_1, translation_1, date_time)
            db.execute("INSERT INTO database (user_id, source, target, datetime) VALUES (?, ?, ?, ?)",
                   user_id, word_2, translation_2, date_time)
            db.execute("INSERT INTO database (user_id, source, target, datetime) VALUES (?, ?, ?, ?)",
                   user_id, word_3, translation_3, date_time)
        if x == 4:
            db.execute("INSERT INTO database (user_id, source, target, datetime) VALUES (?, ?, ?, ?)",
                   user_id, word_1, translation_1, date_time)
            db.execute("INSERT INTO database (user_id, source, target, datetime) VALUES (?, ?, ?, ?)",
                   user_id, word_2, translation_2, date_time)
            db.execute("INSERT INTO database (user_id, source, target, datetime) VALUES (?, ?, ?, ?)",
                   user_id, word_3, translation_3, date_time)
            db.execute("INSERT INTO database (user_id, source, target, datetime) VALUES (?, ?, ?, ?)",
                   user_id, word_4, translation_4, date_time)

        flash("Added!")

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("add.html")


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
            return apology("invalid username and/or password")

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

@app.route("/play")
@login_required
def play():

    user_id = session["user_id"]

    wsad = db.execute("SELECT source, target FROM database WHERE user_id = ?", user_id)

    przekazanie = []

    for row in wsad:
        key = row["source"]  # You can customize the key based on your requirement
        value = row["target"]  # You can customize the value based on your requirement
        new_dict = {key: value}
        przekazanie.append(new_dict)

    selected_dicts = random.sample(przekazanie, 8)

    # Redirect user to login form
    return render_template("play.html", selected_dicts=selected_dicts)


@app.route("/translate")
def translation():

    return render_template("translate.html")


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():

    # Recall user's id
    user_id = session["user_id"]

    rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "POST":

        # Assign values
        password = request.form.get("password")
        new_password = request.form.get("new_password")
        rpt_new_password = request.form.get("rpt_new_password")

        # Ensure passsword is not blank
        if not password:
            return apology("missing current password")

        elif not check_password_hash(rows[0]["hash"], password):
            return apology("wrong current password")

        # Ensure new_passsword is not blank
        elif not new_password:
            return apology("missing new password")

        # Ensure new_passsword differs from old(current one)
        elif password == new_password:
            return apology("must provide unique password")

        # Ensure rpt_new_passsword is not blank
        elif not rpt_new_password:
            return apology("missing repeated new password")

        # Ensure new_passsword differs from old(current one)
        elif rpt_new_password != new_password:
            return apology("must provide the same passwords")

        # Change password in users database
        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(new_password), user_id)

        # Flash the change
        flash("Password Changed!")

        # Redirect user to the homepage
        return redirect("/")

    else:
        return render_template("change.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user """

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Set names
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username")

        # Ensure password was submitted
        if not password:
            return apology("missing password")

        # Ensure password and confirmation are the same
        if not confirmation or password != confirmation:
            return apology("passwords don't match")

        if len(db.execute("SELECT username FROM users where username = ?", username)) != 0:
            return apology("username is not available")
        else:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))

        # Select user's 'id' who's just registered
        user = db.execute("SELECT id FROM users WHERE username = ?", username)

        # Remember which user has logged in
        session["user_id"] = user[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/remove", methods=["GET", "POST"])
def delete():

    # Recall user's id
    user_id = session["user_id"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "GET":

        # modify transactions list
        flshcrd_list = db.execute("SELECT source FROM database WHERE user_id = ? GROUP BY source ORDER BY source", user_id)

        return render_template("remove.html", flshcrd_list=flshcrd_list)

    else:

        # Set names
        word = request.form.get("word")

        # Check time and date
        date_time = datetime.datetime.now(pytz.timezone("Europe/Warsaw"))

        # Check user's amount of credits
        funds = db.execute("SELECT credits FROM users WHERE id = ?", user_id)[0]["credits"]

        # Assigns a list of dicts of user's stocks
        symbols = db.execute("SELECT source FROM database WHERE user_id = ? GROUP BY source", user_id)

        # Create an empty list which is going to be filled with symbols of shares the user currently ownes
        symb = []

        # Fill the list with symbols of shares the user currently ownes
        for row in symbols:
            symb.append(row["source"])

        # Ensure symbol was submitted
        if not word:
            return apology("missing word")

        # Ensure allowed symbol was submitted
        elif word not in symb:
            return apology("word is not in your flashcards")

        # Update 'cash' field in users
        db.execute("UPDATE users SET credits = ? WHERE id = ?", 1 + funds, user_id)

        # Remove the flashcard
        db.execute("DELETE FROM database WHERE user_id = ? AND source = ?", user_id, word)

        flash("Flashcard has been removed!")

        # Redirect user to home page
        return redirect("/")