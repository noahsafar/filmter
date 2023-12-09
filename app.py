import os
import time

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from datetime import timedelta
from threading import Thread
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import fetch_movies, login_required

# Configure app
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem instead of signed cookies
app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=5)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///filmter.db")


def check_activity():
    """Log user out after 5 minutes of inactivity"""

    while True:
        time.sleep(60)
        last_activity_time = session.get("last_activity")
        if last_activity_time and (time.time() - last_activity_time) > 300:
            session.clear()


if __name__ == "__main__":
    activity_checker = Thread(target=check_activity)
    activity_checker.start()

    # Run the Flask app
    app.run(debug=True)


# Dictionary that maps genre IDs with corresponding genre names
genre_mapping = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Science Fiction",
    10770: "TV Movie",
    53: "Thriller",
    10752: "War",
    37: "Western",
}


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
    """Homepage where user can search through movies"""

    # Query database for user
    name = db.execute("SELECT name FROM users WHERE id = ?", session["user_id"])

    # Redirect user to homepage
    return render_template("index.html", name=name)


@app.route("/results", methods=["GET"])
@login_required
def results():
    """Return list of movies that the keywords apply to"""

    # Store keywords the user entered
    keywords = request.args.get("keywords")

    # Handle no keywords
    if not keywords:
        name = db.execute("SELECT name FROM users WHERE id = ?", session["user_id"])
        message = "Please enter a keyword!"
        return render_template("index.html", name=name, message=message)

    # Fetch movie list from database
    movie_data = fetch_movies(keywords)

    # Display movie search results
    if movie_data:
        return render_template(
            "results.html", movies=movie_data, genre_mapping=genre_mapping
        )

    # Handle no results
    if not movie_data:
        return render_template("results.html")


@app.route("/add_watch", methods=["POST"])
@login_required
def add_watch():
    """Add element to want-to-watch list"""

    # Get and store elements for SQL table
    id = request.form.get("id")
    title = request.form.get("title")
    poster_path = request.form.get("poster_path")
    genre_ids = request.form.get("genre_ids")
    overview = request.form.get("overview")
    vote_average = request.form.get("vote_average")
    vote_count = request.form.get("vote_count")
    release_date = request.form.get("runtime")

    # Insert movie data into watchlist database
    db.execute(
        "INSERT INTO watchlist (user_id, id, title, poster_path, genre_ids, overview, vote_average, vote_count, release_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        session["user_id"],
        id,
        title,
        poster_path,
        genre_ids,
        overview,
        vote_average,
        vote_count,
        release_date,
    )

    # Redirect user to watchlist
    return redirect("/want-to-watch")


@app.route("/add_watched", methods=["POST"])
@login_required
def add_watched():
    """Add element to watched-list"""

    # Get and store elements for SQL table
    id = request.form.get("id")
    title = request.form.get("title")
    poster_path = request.form.get("poster_path")
    genre_ids = request.form.get("genre_ids")
    overview = request.form.get("overview")
    vote_average = request.form.get("vote_average")
    vote_count = request.form.get("vote_count")
    release_date = request.form.get("runtime")

    # Insert movie data into watched-list database
    db.execute(
        "INSERT INTO watchedlist (user_id, id, title, poster_path, genre_ids, overview, vote_average, vote_count, release_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        session["user_id"],
        id,
        title,
        poster_path,
        genre_ids,
        overview,
        vote_average,
        vote_count,
        release_date,
    )

    # Redirect user to watched-list
    return redirect("/watched")


@app.route("/want-to-watch")
@login_required
def wanttowatch():
    """Display list of movies that user added as want-to-watch"""

    # Query database
    watchlist = db.execute(
        "SELECT * FROM watchlist WHERE user_id = ?", session["user_id"]
    )

    # Redirect user to watchlist
    return render_template(
        "want-to-watch.html", watchlist=watchlist, genre_mapping=genre_mapping
    )


@app.route("/watched")
@login_required
def watched():
    """Display list of movies that user added as watched"""

    # Query database
    watchedlist = db.execute(
        "SELECT * FROM watchedlist WHERE user_id = ?", session["user_id"]
    )

    # Redirect user to watched-list
    return render_template(
        "watched.html", watchedlist=watchedlist, genre_mapping=genre_mapping
    )


@app.route("/remove_watch", methods=["POST"])
@login_required
def remove_watch():
    """Remove element from want-to-watch list"""

    # Store movie ID
    link = request.form.get("id")

    # Remove element from watchlist database
    db.execute("DELETE FROM watchlist WHERE id = (?)", link)

    # Redirect user to watchlist
    return redirect("/want-to-watch")


@app.route("/remove_watched", methods=["POST"])
@login_required
def remove_watched():
    """Remove element from watched-list"""

    # Store movie ID
    link = request.form.get("id")

    # Remove element from watched-list database
    db.execute("DELETE FROM watchedlist WHERE id = (?)", link)

    # Redirect user to watched-list
    return redirect("/watched")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Acess username and password that the user entered
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username and password were submitted
        if not username or not password:
            message = "Please enter a valid username and password!"
            return render_template("login.html", message=message)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1:
            message = "Please enter a valid username and password!"
            return render_template("login.html", message=message)

        # Check user's password hash
        if check_password_hash(rows[0]["hash"], password):
            # Keep track of the logged-in user
            session["user_id"] = rows[0]["id"]

            # Redirect user to home page
            return redirect("/")

        else:
            message = "The entered password is incorrect!"
            return render_template("login.html", message=message)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Access name, username, password & confirmation that the user entered
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Make sure user provided name, username, password and confirmation
        if not name or not username or not password or not confirmation:
            message = "Please fill out all fields!"
            return render_template("register.html", message=message)

        # Make sure username is alphanumeric
        if not username.isalnum():
            message = "Username should only consist of letters and numbers!"
            return render_template("register.html", message=message)

        # Make sure password is at least 8 characters
        if len(password) < 8:
            message = "Password should be at least eight characters long!"
            return render_template("register.html", message=message)

        # Make sure password and confirmation match
        if password != confirmation:
            message = "Password and password confirmation do not match!"
            return render_template("register.html", message=message)

        # Hash user's password
        hashed_password = generate_password_hash(password)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Make sure username does not already exist
        if len(rows) != 0:
            message = "Username has already been taken."
            return render_template("register.html", message=message)

        # Insert the data into database
        user = db.execute(
            "INSERT INTO users (name, username, hash) VALUES (?, ?, ?)",
            name,
            username,
            hashed_password,
        )

        # Keep track of the logged-in user
        session["user_id"] = user

        # Redirect user to homepage
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Display registration form
        return render_template("register.html")


@app.route("/account", methods=["GET", "POST"])
def account():
    """Let user change information"""

    # Query database for user
    rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    user_name = rows[0]["name"]
    user_username = rows[0]["username"]

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        # Make the "Update Name" tab automatically active
        message = " "
        return render_template(
            "account.html",
            rows=rows,
            name=user_name,
            username=user_username,
            message=message,
        )

    # User reached route via POST (as by submitting a form via POST)
    else:
        # Update name
        name = request.form.get("change_name")
        if name:
            db.execute(
                "UPDATE users SET name = ? WHERE id = ?", name, session["user_id"]
            )
            user_name = name
            message = "Name has been changed successfully!"
            return render_template(
                "account.html",
                rows=rows,
                message=message,
                name=user_name,
                username=user_username,
            )

        # Update username
        username = request.form.get("change_username")
        if username:
            if not username.isalnum():
                message_2 = "Username should only consist of letters and numbers!"
                return render_template(
                    "account.html",
                    rows=rows,
                    message=message_2,
                    name=user_name,
                    username=user_name,
                )
            try:
                db.execute(
                    "UPDATE users SET username = ? WHERE id = ?",
                    username,
                    session["user_id"],
                )
                user_username = username
            except:
                message_2 = "Username has already been taken!"
                return render_template(
                    "account.html",
                    rows=rows,
                    message_2=message_2,
                    username=user_username,
                    name=user_name,
                )
            message_2 = "Username has been changed successfully!"
            return render_template(
                "account.html",
                rows=rows,
                message_2=message_2,
                username=user_username,
                name=user_name,
            )

        # Update password
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        password = generate_password_hash(new_password)
        confirm_password = request.form.get("confirm_password")
        if old_password and new_password and confirm_password:
            if len(new_password) < 8:
                message_3 = "Password should be at least eight characters long!"
                return render_template(
                    "account.html",
                    rows=rows,
                    message_3=message_3,
                    username=user_username,
                    name=user_name,
                )
            if not check_password_hash(password, confirm_password):
                message_3 = "New password and confirmation don't match!"
                return render_template(
                    "account.html",
                    rows=rows,
                    message_3=message_3,
                    username=user_username,
                    name=user_name,
                )
            db.execute(
                "UPDATE users SET hash = ? WHERE id = ?", password, session["user_id"]
            )
            message_3 = "Password has been changed successfully!"
            return render_template(
                "account.html",
                rows=rows,
                message_3=message_3,
                username=user_username,
                name=user_name,
            )

        # Redirect user if they don't update any information
        return redirect("/")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
