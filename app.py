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


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
# Function to get quotes
@app.route("/get_quotes")
def get_quotes():
    popular = True
    qotd = mongo.db.quotes.find_one()
    page = request.args.get('page', 1, type=int)
    limit = int(5)
    skips = limit * (page - 1)
    final_page = (mongo.db.quotes.count_documents({}))/(limit-1)
    pages = range(1, int(final_page + 2))
    quotes = mongo.db.quotes.find().sort("Popularity", -1).skip(skips).limit(limit)
    try:
        # if user logged in 
        if session["user"]:
            # set username value
            username = session["user"]
            # get array of id's for users favourite quotes
            users_fav_quotes = mongo.db.users.find_one({"username": session["user"]})["fav_quote_ids"]
            fav_quotes1 = []
            fav_quotes2 = []
            for x in users_fav_quotes:
                try:
                    # add all favourite quotes in object id format to fav_quotes1
                    fav_quotes1.append(ObjectId(x))
                    # Store all favourited quotes for comparison
                    fav_quotes2.append(x)
                # if not in object id format, pass
                except:
                    pass
            # if user has favourite quotes
            if fav_quotes1:
                # update the quotes and pages with users favourites
                fav_quotes = mongo.db.quotes.find({"_id": {"$in":  fav_quotes1}})
                # update the quotes documents
                quotes = fav_quotes
                # So HTML can identify user is logged in
                popular = False
                # Update pagitation for updated quotes
                final_page = (quotes.count())/(limit-1)
                pages = range(1, int(final_page + 2))
    # if session["user"] not recognised, user is logged out
    except KeyError:
        username=None
        fav_quotes2 = []
    return render_template(
        'quotes.html', 
        quotes=quotes,
        page=page,
        pages=pages,
        limit=limit, 
        qotd=qotd,
        final_page=final_page,
        popular=popular,
        username=username,
        fav_quotes2=fav_quotes2
    )

# function to return all quotes for logged in users
@app.route("/get_all_quotes")
def get_all_quotes():
    popular = True
    qotd = mongo.db.quotes.find_one()
    page = request.args.get('page', 1, type=int)
    limit = int(5)
    skips = limit * (page - 1)
    final_page = (mongo.db.quotes.count_documents({}))/(limit-1)
    pages = range(1, int(final_page + 2))
    quotes = mongo.db.quotes.find().sort("Popularity", -1).skip(skips).limit(limit)
    # feed through favoutite id's so only favourite stars are checked
    try:
        # if user logged in 
        if session["user"]:
            # set username value
            username=session["user"]
            # So HTML can identify user is logged in
            popular = False
            # get array of id's for users favourite quotes
            users_fav_quotes = mongo.db.users.find_one({"username": session["user"]})["fav_quote_ids"]
            fav_quotes2 = []
            # Extract quote id's and append to list
            for x in users_fav_quotes:
                try:
                    fav_quotes2.append(x)
                # if not in object id format, pass
                except:
                    pass
    # if session["user"] not recognised, user is logged out
    except KeyError:
        username=None
        popular = True
        fav_quotes2 = []
    return render_template(
        'quotes.html', 
        quotes=quotes,
        page=page,
        pages=pages,
        limit=limit, 
        qotd=qotd,
        final_page=final_page,
        popular=popular,
        username=username,
        fav_quotes2=fav_quotes2
    )

# https://www.youtube.com/watch?v=XYx5sIbU8B4
# https://www.youtube.com/watch?v=v2TSTKlrPwo
@app.route("/add_fav_quote", methods=["GET", "POST"])        # is "Get" necessary?
# funciton to update db with favourite quotes when star is checked
def add_fav_quote():
    # extract quote id from checkbox id
    quote_id = request.form['Checkbox'].split('_')[0][15:]
    # extract username from checkbox id
    user = request.form['Checkbox'].split('_')[1]
    # if the request is recieved
    if request.method == "POST":
        # if check box is checked
        if request.form['Status'] == 'true':
            # Add quote id to users db
            mongo.db.users.update_one({"username": user},{ "$addToSet": { "fav_quote_ids": quote_id}})
        # else (box is unchecked)
        else:
            # Remove quote if from users db
            mongo.db.users.update_one({"username": user},{ "$pull": { "fav_quote_ids": quote_id}})
    # Get 505 error when return None?
    return "hi"
    

@app.route("/get_authors")
# Function to get authors
def get_authors():
    page = request.args.get('page', 1, type=int)
    limit = int(5)
    skips = limit * (page - 1)
    final_page = (mongo.db.authors.count_documents({}))/(limit-1)
    pages = range(1, int(final_page + 2))
    # find authors for display box
    authors1 = mongo.db.authors.find().skip(skips).limit(limit)
    # Find authors for index
    authors2 = mongo.db.authors.find().sort("Author")
    try:
        # if user logged in 
        if session["user"]:
            # get array of id's for users favourite quotes
            users_fav_authors = mongo.db.users.find_one({"username": session["user"]})["fav_author_ids"]
            fav_authors2 = []
            # Extract author id's and append to list
            for x in users_fav_authors:
                try:
                    fav_authors2.append(x)
                # if not in object id format, pass
                except:
                    pass
    # if session["user"] not recognised, user is logged out
    except KeyError:
        fav_authors2 = []
    return render_template("authors.html", 
        authors1=authors1, 
        authors2=authors2,
        page=page,
        pages=pages,
        limit=limit,
        final_page=final_page,
        fav_authors2=fav_authors2)


@app.route("/get_all_authors")
# Function to get authors
def get_all_authors():
    return None


@app.route("/add_fav_author", methods=["GET", "POST"])        # is "Get" necessary?
# funciton to update db with favourite authors when star is checked
def add_fav_author():
    # extract author id from checkbox id
    author_id = request.form['Checkbox'].split('_')[0][15:]
    # extract username from checkbox id
    user = request.form['Checkbox'].split('_')[1]
    # if the request is recieved
    if request.method == "POST":
        # if check box is checked
        if request.form['Status'] == 'true':
            # Add author id to users db
            mongo.db.users.update_one({"username": user},{ "$addToSet": { "fav_author_ids": author_id}})
        # else (box is unchecked)
        else:
            # Remove author if from users db
            mongo.db.users.update_one({"username": user},{ "$pull": { "fav_author_ids": author_id}})
    # Get 505 error when return None?
    return "hi"    


@app.route("/search_quotes", methods=["GET", "POST"])
# Function to search quotes
def search_quotes():
    popular = True
    qotd = mongo.db.quotes.find_one()
    query = request.form.get("query")
    page = request.args.get('page', 1, type=int)
    limit = int(5)
    skips = limit * (page - 1)
    final_page = (mongo.db.quotes.count_documents(
        {"$text": {"$search": query}}))/(limit-1)
    pages = range(1, int(final_page + 2))
    quotes = mongo.db.quotes.find(
        {"$text": {"$search": query}}).skip(skips).limit(limit)
    # feed through favoutite id's so only favourite stars are checked
    try:
        # if user logged in 
        if session["user"]:
            # set username value
            username=session["user"]
            # So HTML can identify user is logged in
            popular = False
            # get array of id's for users favourite quotes
            users_fav_quotes = mongo.db.users.find_one({"username": session["user"]})["fav_quote_ids"]
            fav_quotes2 = []
            # Extract quote id's and append to list
            for x in users_fav_quotes:
                try:
                    fav_quotes2.append(x)
                # if not in object id format, pass
                except:
                    pass
    # if session["user"] not recognised, user is logged out
    except KeyError:
        username=None
        popular = True
        fav_quotes2 = []
    return render_template('quotes.html',
                           quotes=quotes,
                           page=page,
                           pages=pages,
                           limit=limit,
                           qotd=qotd,
                           final_page=final_page,
                           username=username,
                           fav_quotes2=fav_quotes2,
                           popular = popular)


@app.route("/search_authors", methods=["GET", "POST"])
# Function to search authors
def search_authors():
    # get searched query
    searchTerm = request.form.get("query_author")
    # search query to index
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
