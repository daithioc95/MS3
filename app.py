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
from datetime import date, datetime


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
    # start date - todays date
    qotd = mongo.db.quotes.find_one()
    page = request.args.get('page', 1, type=int)
    limit = int(5)
    skips = limit * (page - 1)
    # final_page = math.ceil((mongo.db.quotes.count_documents({}))/(limit))
    # pages = range(1, int(final_page + 1))
    # Limit pages with updated db
    final_page = 20 # change to 10
    pages = range(1, int(final_page + 1))
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
                final_page = math.ceil((quotes.count())/(limit))
                pages = range(1, int(final_page + 1))
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
    return "Method not supported"
    

@app.route("/get_authors", methods=["GET"])
# Function to get authors
def get_authors():
    get_fav = request.args.get('get_fav')
    page = request.args.get('page', 1, type=int)
    limit = int(6)
    skips = limit * (page - 1)
    # final_page = math.ceil((mongo.db.authors.count_documents({}))/(limit))
    # pages = range(1, int(final_page + 1))
    # Limit pages with updated db
    final_page = 20 # change back to 10
    pages = range(1, int(final_page + 1))
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
                final_page = math.ceil((authors1.count())/(limit))
                pages = range(1, int(final_page + 1))
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
    return "Method not supported"  


@app.route("/add_fav_book", methods=["GET", "POST"])        # is "Get" necessary?
# funciton to update db with favourite books when star is checked
def add_fav_book():
    # extract book id from checkbox id
    book_id = request.form['Checkbox'].split('_')[0][15:]
    # extract username from checkbox id
    user = request.form['Checkbox'].split('_')[1]
    # if the request is recieved
    if request.method == "POST":
        # if check box is checked
        if request.form['Status'] == 'true':
            # Add book id to users db
            mongo.db.users.update_one({"username": user},{ "$addToSet": { "fav_book_ids": book_id}})
        # else (box is unchecked)
        else:
            # Remove book if from users db
            mongo.db.users.update_one({"username": user},{ "$pull": { "fav_book_ids": book_id}})
    # Get 505 error when return None?
    return "Method not supported"  


def get_starred(username, category):
    # can we pass the below as a function to get fav_authors2?
    # get array of id's for users favourite authors
    if category == "author":
        users_fav = mongo.db.users.find_one({"username": username})["fav_author_ids"]
    if category == "quote":
        users_fav = mongo.db.users.find_one({"username": username})["fav_quote_ids"]
    if category == "book":
        users_fav = mongo.db.users.find_one({"username": username})["fav_book_ids"]
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
    if category == "book":
        users_fav = mongo.db.users.find_one({"username": username})["fav_book_ids"]
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
    generated = request.args.get('generated')
    if generated == "yes":
        query = request.form.get("query_quote")
    else:
        query = request.args.get('query_quote')
    qotd = mongo.db.quotes.find_one()
    page = request.args.get('page', 1, type=int)
    limit = int(5)
    skips = limit * (page - 1)
    quotes = mongo.db.quotes.find(
        {"$text": {"$search": query}}).skip(skips).limit(limit)
    searched = True
    # limit pages to 10 as results excessive
    if math.ceil((mongo.db.quotes.count_documents(
        {"$text": {"$search": query}}))/(limit)) < 10:
        final_page =math.ceil((mongo.db.quotes.count_documents(
        {"$text": {"$search": query}}))/(limit))
    else:
        final_page = 10
    pages = range(1, int(final_page + 1))
    # Limit pages with updated db
    try:
        # if user logged in 
        if session["user"]:
            # get array of id's for users favourite quotes
            starred = get_starred(session["user"], "quote")
    # if session["user"] not recognised, user is logged out
    except KeyError:
        starred = []
    return render_template('quotes.html',
                           quotes=quotes,
                           page=page,
                           pages=pages,
                           limit=limit,
                           qotd=qotd,
                           final_page=final_page,
                           fav_quotes2=starred,
                           query_quote = query,
                           searched=searched)


@app.route("/search_authors", methods=["GET", "POST"])
# Function to search authors
def search_authors():
    generated = request.args.get('generated')
    if generated == "yes":
        searchTerm = request.form.get("query_author")
    else:
        searchTerm = request.args.get('query_author')
    page = request.args.get('page', 1, type=int)
    limit = int(6)
    skips = limit * (page - 1)
    # get searched query
    # final_page = math.ceil((mongo.db.authors.count_documents(
    #     {"$text": {"$search": searchTerm}}))/(limit-1))
    # pages = range(1, int(final_page + 1))
    # Limit pages with updated db
    final_page = 10
    # search query to index
    authors1 = mongo.db.authors.find({"$text": {"$search":searchTerm }}).skip(skips).limit(limit)
    # feed through favoutite id's so only favourite stars are checked
    searched = True
    final_page =math.ceil((mongo.db.authors.count_documents(
    {"$text": {"$search": searchTerm}}))/(limit))
    pages = range(1, int(final_page + 1))
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
                            fav_authors2=starred,
                            query_author = searchTerm,
                            searched=searched)


@app.route("/author_profile/<Author>", methods=["GET", "POST"])
def author_profile(Author):
    limit = int(6)
    page = request.args.get('page', 1, type=int)
    skips = limit * (page - 1)
    author = mongo.db.authors.find_one(
        {"Author": Author})
    quotes = mongo.db.quotes.find({"Author": Author}).skip(skips).limit(limit)
    final_page = math.ceil((mongo.db.quotes.count_documents({"Author": Author}))/(limit))
    # final_page = math.ceil((mongo.db.quotes.find({"Author": Author}))/(limit-1))
    pages = range(1, int(final_page + 1))
    try:
        Categories = mongo.db.authors.find_one({"Author": Author})["Categories"]
    except KeyError:
        Categories = []
    similar_authors = mongo.db.authors.find({"Categories": {"$in":  Categories}}).limit(6)
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
                            fav_authors2=fav_authors2,
                            page=page, 
                            pages=pages,
                            limit=limit,
                            final_page=final_page)


@app.route("/get_books", methods=["GET"])
# Function to get books
def get_books():
    get_fav = request.args.get('get_fav')
    # page = request.args.get('page', 1, type=int)
    # limit = int(6)
    # skips = limit * (page - 1)
    # final_page = math.ceil((mongo.db.authors.count_documents({}))/(limit))
    # pages = range(1, int(final_page + 1))
    # Limit pages with updated db
    # final_page = 10
    # pages = range(1, int(final_page + 1))
    # find authors for display box
    # authors1 = mongo.db.authors.find().skip(skips).limit(limit)
    # Find authors for index
    books = mongo.db.books.find().limit(30)
    try:
        # if user logged in 
        if session["user"]:
            # get array of id's for users favourite authors
            fav_books1 = get_favourites(session["user"], "book")
            fav_books2 = get_starred(session["user"], "book")
            if fav_books1 and get_fav != "No":
                # update the books and pages with users favourites
                fav_books = mongo.db.books.find({"_id": {"$in":  fav_books1}}).limit(30)
                # update the books documents
                books = fav_books
                # Update pagitation for updated quotes
                # final_page = math.ceil((authors1.count())/(limit))
                # pages = range(1, int(final_page + 1))
    # if session["user"] not recognised, user is logged out
    except KeyError:
        fav_books2 = []
    return render_template("books.html", 
        books=books, 
        # authors2=authors2,
        # page=page,
        # pages=pages,
        # limit=limit,
        # final_page=final_page,
        # fav_authors2=fav_authors2,
        fav_books2=fav_books2,
        get_fav=get_fav)


@app.route("/search_books", methods=["GET", "POST"])
# Function to search books
def search_books():
    generated = request.args.get('generated')
    if generated == "yes":
        searchTerm = request.form.get("query_book")
    else:
        searchTerm = request.args.get('query_book')
    # page = request.args.get('page', 1, type=int)
    # limit = int(6)
    # skips = limit * (page - 1)
    # get searched query
    # final_page = math.ceil((mongo.db.authors.count_documents(
    #     {"$text": {"$search": searchTerm}}))/(limit-1))
    # pages = range(1, int(final_page + 1))
    # Limit pages with updated db
    # final_page = 10
    # pages = range(1, int(final_page + 1))
    # search query to index
    books = mongo.db.books.find({"$text": {"$search":searchTerm }}).limit(30)
    # feed through favoutite id's so only favourite stars are checked
    searched = True
    try:
        # if user logged in 
        if session["user"]:
            starred = get_starred(session["user"], "book")
    # if session["user"] not recognised, user is logged out
    except KeyError:
        starred = []
    return render_template('books.html', 
                            books=books, 
                            # page=page, 
                            # pages=pages,
                            # limit=limit,
                            # final_page=final_page,
                            fav_books2=starred,
                            query_book = searchTerm,
                            searched=searched)


@app.route("/book_profile/<Book>", methods=["GET", "POST"])
def book_profile(Book):
    limit = int(6)
    page = request.args.get('page', 1, type=int)
    skips = limit * (page - 1)
    book = mongo.db.books.find_one({"Book": Book})
    quotes = mongo.db.quotes.find({"Book": Book}).skip(skips).limit(limit)
    # author = mongo.db.quotes.find({"Book": Book})["Author"]
    final_page = math.ceil((mongo.db.quotes.count_documents({"Book": Book}))/(limit))
    # final_page = math.ceil((mongo.db.quotes.find({"Author": Author}))/(limit-1))
    pages = range(1, int(final_page + 1))
    # Categories = mongo.db.quotes.find_one({"Book": Book})["Category"]
    # categories = mongo.db.books.find_one({"Book": Book})["Categories"]
    author = mongo.db.books.find_one({"Book": Book})["Author"]
    authors_books = mongo.db.authors.find_one({"Author": author})["Books"]
    try:
        # if user logged in 
        if session["user"]:
            fav_quotes2 = get_starred(session["user"], "quote")
            fav_authors2 = get_starred(session["user"], "author")
            fav_books2 = get_starred(session["user"], "book")
    # if session["user"] not recognised, user is logged out
    except KeyError:
        fav_quotes2 = []
        fav_authors2 = []
        fav_books2 = []
    return render_template("indiv_book.html",
                            # author=author, 
                            book=book,
                            quotes=quotes, 
                            authors_books=authors_books,
                            fav_quotes2=fav_quotes2, 
                            fav_books2=fav_books2, 
                            # authors_books=authors_books,
                            # fav_authors2=fav_authors2,
                            page=page, 
                            pages=pages,
                            limit=limit,
                            final_page=final_page
                            )


@app.route("/get_mood")
def get_mood():
    return render_template("mood.html")

@app.route("/generate_mood", methods=["GET", "POST"])
def generate_mood():
    page = request.args.get('page', 1, type=int)
    limit = int(5)
    skips = limit * (page - 1)
    generated = request.args.get('generated')
    # if form initialised get list from for
    if generated == "yes":
        # checked_buttons = request.form.getlist('mood-button')
        search_tags = request.form.getlist('mood-button')
    # if form on next pages pass previously initialised tags
    else:
        # checked_buttons = request.args.getlist('search_tags')
        search_tags = request.args.getlist('search_tags')
    # print(checked_buttons)
    # final_page = math.ceil((mongo.db.quotes.count_documents({"$text": {"$search": search_tags}}))/(limit))
    # pages = range(1, int(final_page + 1))
    # Limit pages with updated db
    final_page = 10
    pages = range(1, int(final_page + 1))
    quotes = mongo.db.quotes.find({"$text": {"$search": str(search_tags)}}).skip(skips).limit(limit)
    # rename to avoid confustion?
    generated = True
    try:
        # if user logged in 
        if session["user"]:
            # get array of id's for users favourite quotes
            starred = get_starred(session["user"], "quote")
    # if session["user"] not recognised, user is logged out
    except KeyError:
        starred = []
    return render_template("mood.html", 
                            quotes=quotes, 
                            fav_quotes2=starred, 
                            page=page, 
                            pages=pages, 
                            final_page=final_page, 
                            generated=generated,
                            search_tags=search_tags,)
                            # checked_buttons=checked_buttons


@app.route("/share_quote/<_id>", methods=["GET", "POST"])
def share_quote(_id):
    quote = mongo.db.quotes.find_one({"_id": ObjectId(_id)})
    return render_template("share_quote.html",
                        quote=quote)


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
            "email": request.form.get("email").lower(),
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
    user = mongo.db.users.find_one(
        {"username": session["user"]})
    fav_quotes1 = get_favourites(session["user"], "quote")
    quotes = mongo.db.quotes.find({"_id": {"$in":  fav_quotes1}})
    fav_quotes2 = get_starred(session["user"], "quote")
    fav_authors1 = get_favourites(session["user"], "author")
    authors = mongo.db.authors.find({"_id": {"$in":  fav_authors1}})
    fav_authors2 = get_starred(session["user"], "author")
    fav_books = get_favourites(session["user"], "book")
    books = mongo.db.books.find({"_id": {"$in":  fav_books}})
    if session["user"]:
        return render_template("profile.html", 
                                user=user,
                                quotes=quotes, 
                                fav_quotes2=fav_quotes2, 
                                authors=authors, 
                                fav_authors2=fav_authors2,
                                books=books)

    return redirect(url_for("login"))


@app.route("/comment", methods=["GET", "POST"])
def comment():
    if request.method == "POST":
        username = session["user"]
        comment = request.form.get("comment")
        section = request.args.get('section')
        today = datetime.today()
        date = today.strftime("%d/%m/%Y")
        if section == "authors":
            Author = request.args.get('Author')
            mongo.db.authors.update_one({"Author": Author},{ "$addToSet": { "Comments": {'text':comment,'user':username,'date':date}}})
            return redirect(url_for("author_profile", Author=Author))
        if section == "books":
            Book = request.args.get('Book')
            mongo.db.books.update_one({"Book": Book},{ "$addToSet": { "Comments": {'text':comment,'user':username,'date':date}}})
            return redirect(url_for("book_profile", Book=Book))

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
