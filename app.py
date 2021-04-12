import os
import pymongo
import json
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
# MONGO_URI = os.environ.get("MONGO_URI")
# DATABASE = "ms3_quotes"
# COLLECTION_QUTOES = "quotes"
# COLLECTION_AUTHORS = "authors"
# COLLECTION_USERS = "users"
# def mongo_connect(url):
#     try:
#         conn = pymongo.MongoClient(url)
#         print("Mongo is connected to app.py")
#         return conn
#     except pymongo.errors.ConnectionFailure as e:
#         print("Could not connect to MongoDB: %s") % e
# conn = mongo_connect(MONGO_URI)
# coll1 = conn[DATABASE][COLLECTION_QUTOES]
# coll2 = conn[DATABASE][COLLECTION_AUTHORS]
# coll3 = conn[DATABASE][COLLECTION_USERS]


# documents_authors = coll1.find({},{ "_id": 0, "Author": 1})
# documents = coll1.find()

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


# https://www.youtube.com/watch?v=XYx5sIbU8B4
# https://www.youtube.com/watch?v=v2TSTKlrPwo
@app.route("/add_fav_quote", methods=["GET", "POST"])        # is "Get" necessary?
def add_fav_quote():
    quote_id = request.form['Checkbox'].split('_')[0][15:]
    user = request.form['Checkbox'].split('_')[1]
    if request.method == "POST":
        # if check box is checked
        if request.form['Status'] == 'true':
            # Add quote id to users db
            mongo.db.users.update_one({"username": user},{ "$addToSet": { "fav_quote_ids": quote_id}})
        # else (box is unchecked)
        else:
            # Remove quote if from users db
            mongo.db.users.update_one({"username": user},{ "$pull": { "fav_quote_ids": quote_id}})
    return "hi"


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


@app.route("/search_quotes", methods=["GET", "POST"])
def search_quotes():
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


@app.route("/search_authors", methods=["GET", "POST"])
def search_authors():
    searchTerm = request.form.get("query_author")
    print(mongo.db.authors.find({"$text": {"$search":searchTerm }}))
    # maximum = math.floor( (mongo.db.quotes.count_documents({})) / limit - 1)
    authors1 = mongo.db.authors.find({"$text": {"$search":searchTerm }})
    return render_template('authors.html', 
        authors1=authors1)


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
            "password": generate_password_hash(request.form.get("password")),
            "fav_quote_ids": [],
            "fav_author_ids": [],
            "fav_book_ids": []
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