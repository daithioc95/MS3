import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, request)
from flask_pymongo import PyMongo
from flask_paginate import Pagination, get_page_args
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import math
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_quotes")
# def get_quotes():
#     qotd = mongo.db.quotes.find_one()
#     quotes = mongo.db.quotes.find().sort("Popularity", -1)
#     return render_template("quotes.html", quotes=quotes, qotd=qotd) 
def get_quotes():
    qotd = mongo.db.quotes.find_one()
    page = request.args.get('page', 1, type=int)
    limit=int(5)
    skips = limit * (page - 1)
    # maximum = math.floor( (mongo.db.quotes.count_documents({})) / limit - 1)
    final_page = (mongo.db.quotes.count_documents({}))/(limit-1)
    pages = range(1, int(final_page + 2))
    quotes = mongo.db.quotes.find().sort("Popularity", -1).skip(skips).limit(limit)
    return render_template(
        'quotes.html', 
        quotes=quotes,
        page=page,
        pages=pages,
        # maximum=maximum,
        limit=limit, 
        qotd=qotd,
        final_page=final_page
    )

# def get_quotes():
#     #     # https://www.youtube.com/watch?v=PSWf2TjTGNY
#     qotd = mongo.db.quotes.find_one()
#     page = request.args.get('page', 1, type=int)
#     skips = 5 * (page - 1)
#     quotes = mongo.db.quotes.find().sort("Popularity", -1).skip(skips).limit(5)
#     return render_template("quotes.html", quotes=quotes, qotd=qotd, page=page) 


# @app.route("/get_quotes2")
# def get_quotes2():
#     qotd = mongo.db.quotes.find_one()
#     # quotes = mongo.db.quotes.find().sort("Popularity", -1)
#     # https://www.youtube.com/watch?v=PSWf2TjTGNY
#     page = request.args.get('page',1,type=int)
#     posts = Post.query.paginate(page=page, per_page=5)
#     return render_template("quotes_copy.html", posts=posts, qotd=qotd) 


@app.route("/get_authors")
def get_authors():
    authors1 = mongo.db.authors.find()
    authors2 = mongo.db.authors.find().sort("Author")
    return render_template("authors.html", authors1=authors1, authors2=authors2) 


@app.route("/search", methods=["GET", "POST"])
def search():
    qotd = mongo.db.quotes.find_one()
    query = request.form.get("query")
    page = request.args.get('page', 1, type=int)
    limit=int(5)
    skips = limit * (page - 1)
    # maximum = math.floor( (mongo.db.quotes.count_documents({})) / limit - 1)
    final_page = (mongo.db.quotes.count_documents({"$text": {"$search":query }}))/(limit-1)
    pages = range(1, int(final_page + 2))
    quotes = mongo.db.quotes.find({"$text": {"$search":query }}).skip(skips).limit(limit)
    return render_template('quotes.html', 
        quotes=quotes,
        page=page,
        pages=pages,
        limit=limit, 
        qotd=qotd,
        final_page=final_page)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        flash("Welcome, {}".format(
                            request.form.get("username")))
                        return redirect(url_for(
                            "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)