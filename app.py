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
    get_fav = request.args.get('get_fav')
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
            # get array of id's for users favourite quotes
            # get array of id's for users favourite authors
            fav_quotes1 = get_favourites(session["user"], "quote")
            fav_quotes2 = get_starred(session["user"], "quote")
            if fav_quotes1 and get_fav != "No":
                # update the quotes and pages with users favourites
                fav_quotes = mongo.db.quotes.find({"_id": {"$in":  fav_quotes1}}).skip(skips).limit(limit)
                # update the quotes documents
                quotes = fav_quotes
                # Update pagitation for updated quotes
                final_page = (quotes.count())/(limit-1)
                pages = range(1, int(final_page + 2))
    # if session["user"] not recognised, user is logged out
    except KeyError:
        fav_quotes2 = []
    return render_template(
        'quotes.html', 
        quotes=quotes,
        page=page,
        pages=pages,
        limit=limit, 
        qotd=qotd,
        final_page=final_page,
        fav_quotes2=fav_quotes2,
        get_fav=get_fav
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
    

@app.route("/get_authors", methods=["GET"])
# Function to get authors
def get_authors():
    get_fav = request.args.get('get_fav')
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
            # get array of id's for users favourite authors
            fav_authors1 = get_favourites(session["user"], "author")
            fav_authors2 = get_starred(session["user"], "author")
            if fav_authors1 and get_fav != "No":
                # update the authors and pages with users favourites
                fav_authors = mongo.db.authors.find({"_id": {"$in":  fav_authors1}}).skip(skips).limit(limit)
                # update the authors documents
                authors1 = fav_authors
                # Update pagitation for updated quotes
                final_page = (authors1.count())/(limit-1)
                pages = range(1, int(final_page + 2))
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
        fav_authors2=fav_authors2,
        get_fav=get_fav)


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


def get_starred(username, category):
    # can we pass the below as a function to get fav_authors2?
    # get array of id's for users favourite authors
    if category == "author":
        users_fav = mongo.db.users.find_one({"username": username})["fav_author_ids"]
    if category == "quote":
        users_fav = mongo.db.users.find_one({"username": username})["fav_quote_ids"]
    starred = []
    # Extract author id's and append to list
    for x in users_fav:
        try:
            starred.append(x)
        # if not in object id format, pass
        except:
            pass
    return (starred)


def get_favourites(username, category):
        # can we pass the below as a function to get fav_authors2?
    # get array of id's for users favourite authors
    if category == "author":
        users_fav = mongo.db.users.find_one({"username": username})["fav_author_ids"]
    if category == "quote":
        users_fav = mongo.db.users.find_one({"username": username})["fav_quote_ids"]
    favourites = []
    # Extract author id's and append to list
    for x in users_fav:
        try:
            favourites.append(ObjectId(x))
        # if not in object id format, pass
        except:
            pass
    return (favourites)


@app.route("/search_quotes", methods=["GET", "POST"])
# Function to search quotes
def search_quotes():
    qotd = mongo.db.quotes.find_one()
    query = request.form.get("query_quote")
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
            # get array of id's for users favourite quotes
            starred = get_starred(session["user"], "quote")
    # if session["user"] not recognised, user is logged out
    except KeyError:
        fav_quotes2 = []
    return render_template('quotes.html',
                           quotes=quotes,
                           page=page,
                           pages=pages,
                           limit=limit,
                           qotd=qotd,
                           final_page=final_page,
                           fav_quotes2=starred)


@app.route("/search_authors", methods=["GET", "POST"])
# Function to search authors
def search_authors():
    page = request.args.get('page', 1, type=int)
    limit = int(5)
    skips = limit * (page - 1)
    # get searched query
    searchTerm = request.form.get("query_author")
    final_page = (mongo.db.authors.count_documents(
        {"$text": {"$search": searchTerm}}))/(limit-1)
    pages = range(1, int(final_page + 2))
    # search query to index
    authors1 = mongo.db.authors.find({"$text": {"$search":searchTerm }})
    # feed through favoutite id's so only favourite stars are checked
    try:
        # if user logged in 
        if session["user"]:
            starred = get_starred(session["user"], "author")
    # if session["user"] not recognised, user is logged out
    except KeyError:
        starred = []
    return render_template('authors.html', 
                            authors1=authors1, 
                            page=page, 
                            pages=pages,
                            limit=limit,
                            final_page=final_page,
                            fav_authors2=starred)


@app.route("/author_profile/<Author>", methods=["GET", "POST"])
def author_profile(Author):
    author = mongo.db.authors.find_one(
        {"Author": Author})
    quotes = mongo.db.quotes.find({"Author": Author})
    Categories = mongo.db.authors.find_one({"Author": Author})["Categories"]
    similar_authors = mongo.db.authors.find({"Categories": {"$in":  Categories}})
    try:
        # if user logged in 
        if session["user"]:
            fav_quotes2 = get_starred(session["user"], "quote")
            fav_authors2 = get_starred(session["user"], "author")
    # if session["user"] not recognised, user is logged out
    except KeyError:
        fav_quotes2 = []
        fav_authors2 = []
    return render_template("indiv_author.html",
                            author=author, 
                            quotes=quotes, 
                            fav_quotes2=fav_quotes2, 
                            similar_authors=similar_authors,
                            fav_authors2=fav_authors2)


@app.route("/get_mood", methods=["GET", "POST"])
def get_mood():
    quotes = {}
    if request.method == 'POST':
        search_tags = str(request.form.getlist('mood-button'))
        # is this an appropriate way to search an array?
        quotes = list(mongo.db.quotes.find({"$text": {"$search": search_tags}}))
        # feed through favoutite id's so only favourite stars are checked
    try:
        # if user logged in 
        if session["user"]:
            # get array of id's for users favourite quotes
            starred = get_starred(session["user"], "quote")
    # if session["user"] not recognised, user is logged out
    except KeyError:
        starred = []
    return render_template("mood.html", quotes=quotes, fav_quotes2=starred)


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
    fav_quotes1 = get_favourites(session["user"], "quote")
    quotes = mongo.db.quotes.find({"_id": {"$in":  fav_quotes1}})
    fav_quotes2 = get_starred(session["user"], "quote")
    fav_authors1 = get_favourites(session["user"], "author")
    authors = mongo.db.authors.find({"_id": {"$in":  fav_authors1}})
    fav_authors2 = get_starred(session["user"], "author")
    if session["user"]:
        return render_template("profile.html", 
                                username=username, 
                                quotes=quotes, 
                                fav_quotes2=fav_quotes2, 
                                authors=authors, 
                                fav_authors2=fav_authors2)

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
