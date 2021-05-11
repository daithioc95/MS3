import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
# from flask_paginate import Pagination, get_page_args
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import math
from datetime import datetime
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
    # identify is user requested saved favourites
    get_fav = request.args.get('get_fav')
    # formula to extract different date per day
    base = int(20210507)
    today = datetime.today()
    date = int(today.strftime("%Y%m%d"))
    qotd_num = abs(date-base)
    # qotd meand "Quote of the day"
    qotd = mongo.db.quotes.find().skip(qotd_num).limit(1)[0]
    # Pagination Aknowledgement: https://stackoverflow.com/questions/58031816/how-to-display-active-bootstrap-pagination-using-jinja-conditional
    # get page number
    page = request.args.get('page', 1, type=int)
    # limit quotes to 5 results
    limit = int(5)
    # iterate through objects depending on page number
    skips = limit * (page - 1)
    # limit results to 20 pages
    final_page = 20
    pages = range(1, int(final_page + 1))
    # set of quotes to return
    quotes = mongo.db.quotes.find().sort("Popularity", -1).skip(skips).limit(limit)
    # Fail safe for if user is logged out
    try:
        # if user logged in
        if session["user"]:
            # get array of id's for users favourite quotes
            fav_quotes1 = get_favourites(session["user"], "quote")
            # get list of favourite to identify which quotes to show as already favourited
            fav_quotes2 = get_starred(session["user"], "quote")
            # if user has favourites saved and they requested to view them
            if fav_quotes1 and get_fav != "No":
                # update the quotes and pages with users favourites
                fav_quotes = mongo.db.quotes.find(
                    {"_id": {"$in":  fav_quotes1}}).skip(skips).limit(limit)
                # update the quotes documents
                quotes = fav_quotes
                # Update pagitation for updated quotes
                final_page = math.ceil((quotes.count())/(limit))
                pages = range(1, int(final_page + 1))
    # if session["user"] not recognised, user is logged out
    except KeyError:
        # return favquotes2 as empty
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

# Acknowledge below 2 videos in helping with adding fav star info
# https://www.youtube.com/watch?v=XYx5sIbU8B4
# https://www.youtube.com/watch?v=v2TSTKlrPwo

# funciton to update db with favourite quotes when star is checked


@app.route("/add_fav_quote", methods=["GET", "POST"])
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
            mongo.db.users.update_one(
                {"username": user},
                {"$addToSet": {"fav_quote_ids": quote_id}})
        # else (box is unchecked)
        else:
            # Remove quote if unchecked
            mongo.db.users.update_one(
                {"username": user},
                {"$pull": {"fav_quote_ids": quote_id}})
    # To avoid 505 error
    return "Method not supported"


# Function to get authors
@app.route("/get_authors", methods=["GET"])
def get_authors():
    # identify is user requested saved favourites
    get_fav = request.args.get('get_fav')
    # get page number
    page = request.args.get('page', 1, type=int)
    # limit authors to 6 results
    limit = int(6)
    # iterate through objects depending on page number
    skips = limit * (page - 1)
    # limit results to 20 pages
    final_page = 20
    pages = range(1, int(final_page + 1))
    # set of authors to return
    authors1 = mongo.db.authors.find().skip(skips).limit(limit)
    # Fail safe for if user is logged out
    try:
        # if user logged in
        if session["user"]:
            # get array of id's for users favourite authors
            fav_authors1 = get_favourites(session["user"], "author")
            # get list of favourite to identify which authors to show as already favourited
            fav_authors2 = get_starred(session["user"], "author")
            # if user has favourites saved and they requested to view them
            if fav_authors1 and get_fav != "No":
                # update the authors and pages with users favourites
                fav_authors = mongo.db.authors.find(
                    {"_id": {"$in":  fav_authors1}}).skip(skips).limit(limit)
                # update the authors documents
                authors1 = fav_authors
                # Update pagitation for updated quotes
                final_page = math.ceil((authors1.count())/(limit))
                pages = range(1, int(final_page + 1))
    # if session["user"] not recognised, user is logged out
    except KeyError:
        # return fav_authors2 as empty
        fav_authors2 = []
    return render_template("authors.html",
                           authors1=authors1,
                           page=page,
                           pages=pages,
                           limit=limit,
                           final_page=final_page,
                           fav_authors2=fav_authors2,
                           get_fav=get_fav)


# function to update db with favourite authors when star is checked
@app.route("/add_fav_author", methods=["GET", "POST"])
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
            mongo.db.users.update_one(
                {"username": user}, {"$addToSet": {"fav_author_ids": author_id}})
        # else (box is unchecked)
        else:
            # Remove author if unchecked
            mongo.db.users.update_one(
                {"username": user}, {"$pull": {"fav_author_ids": author_id}})
    # Get 505 error when return None?
    return "Method not supported"


# function to update db with favourite books when star is checked
@app.route("/add_fav_book", methods=["GET", "POST"])
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
            mongo.db.users.update_one(
                {"username": user}, {"$addToSet": {"fav_book_ids": book_id}})
        # else (box is unchecked)
        else:
            # Remove book if from users db
            mongo.db.users.update_one(
                {"username": user}, {"$pull": {"fav_book_ids": book_id}})
    # Get 505 error when return None?
    return "Method not supported"

# Function to get favourited items to show as starred (checked)


def get_starred(username, category):
    # if query for Author
    if category == "author":
        # find users favs
        users_fav = mongo.db.users.find_one({"username": username})[
            "fav_author_ids"]
    # if query for Quote
    if category == "quote":
        # find users favs
        users_fav = mongo.db.users.find_one(
            {"username": username})["fav_quote_ids"]
    # if query for Book
    if category == "book":
        # find users favs
        users_fav = mongo.db.users.find_one(
            {"username": username})["fav_book_ids"]
    # list to store favourites
    starred = []
    # Extract author id's and append to list
    for x in users_fav:
        # Fail safe for incorrect formats
        try:
            # add to starred list
            starred.append(x)
        # if not in object id format, pass
        except:
            pass
    # Return list
    return (starred)

# Function to get dictionary of favourited objects to post


def get_favourites(username, category):
    # if query for Author
    if category == "author":
        # find users favs
        users_fav = mongo.db.users.find_one({"username": username})[
            "fav_author_ids"]
    # if query for Quote
    if category == "quote":
        # find users favs
        users_fav = mongo.db.users.find_one(
            {"username": username})["fav_quote_ids"]
    # if query for Book
    if category == "book":
        # find users favs
        users_fav = mongo.db.users.find_one(
            {"username": username})["fav_book_ids"]
    # list to store favourites
    favourites = []
    # Extract author id's and append to list
    for x in users_fav:
        # Fail safe for incorrect formats
        try:
            # add Object to starred list
            favourites.append(ObjectId(x))
        # if not in object id format, pass
        except:
            pass
    # Return list
    return (favourites)


# Function to search quotes
@app.route("/search_quotes", methods=["GET", "POST"])
def search_quotes():
    # if search function just activated
    generated = request.args.get('generated')
    if generated == "yes":
        # extract search query from form
        query = request.form.get("query_quote")
    # For different pages extract query from url
    else:
        query = request.args.get('query_quote')
    # ensure qotd is still defined
    # formula to extract different date per day
    base = int(20210507)
    today = datetime.today()
    date = int(today.strftime("%Y%m%d"))
    qotd_num = abs(date-base)
    # qotd meand "Quote of the day"
    qotd = mongo.db.quotes.find().skip(qotd_num).limit(1)[0]
    # Get page number from url
    page = request.args.get('page', 1, type=int)
    # limit quotes to 5 results
    limit = int(5)
    # iterate through objects depending on page number
    skips = limit * (page - 1)
    # set of quotes to return
    quotes = mongo.db.quotes.find(
        {"$text": {"$search": query}}).skip(skips).limit(limit)
    # if search has been completed
    searched = True
    # limit pages to 10 as results excessive
    if math.ceil((mongo.db.quotes.count_documents(
            {"$text": {"$search": query}}))/(limit)) < 10:
        final_page = math.ceil((mongo.db.quotes.count_documents(
            {"$text": {"$search": query}}))/(limit))
    else:
        final_page = 10
    pages = range(1, int(final_page + 1))
    # get array of id's for users favourite quotes
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
                           query_quote=query,
                           searched=searched)


# Function to search authors
@app.route("/search_authors", methods=["GET", "POST"])
def search_authors():
    # if search function just activated
    generated = request.args.get('generated')
    if generated == "yes":
        # extract search query from form
        searchTerm = request.form.get("query_author")
    # For different pages extract query from url
    else:
        searchTerm = request.args.get('query_author')
    # Get page number from url
    page = request.args.get('page', 1, type=int)
    # limit quotes to 6 results
    limit = int(6)
    # iterate through objects depending on page number
    skips = limit * (page - 1)
    # search query to index
    authors1 = mongo.db.authors.find(
        {"$text": {"$search": searchTerm}}).skip(skips).limit(limit)
    # if search has been completed
    searched = True
    # limit pages to match total documents
    final_page = math.ceil((mongo.db.authors.count_documents(
        {"$text": {"$search": searchTerm}}))/(limit))
    pages = range(1, int(final_page + 1))
    # Fail safe for if user is logged out
    try:
        # if user logged in
        if session["user"]:
            # get array of id's for users favourite quotes
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
                           query_author=searchTerm,
                           searched=searched)


# function for individual author profile
@app.route("/author_profile/<Author>", methods=["GET", "POST"])
def author_profile(Author):
    # limit author quotes to 6 results
    limit = int(6)
    # Get quotes page number from url
    page = request.args.get('page', 1, type=int)
    # iterate through objects depending on page number
    skips = limit * (page - 1)
    # Locate author object
    author = mongo.db.authors.find_one(
        {"Author": Author})
    # set of authors quotes to return
    quotes = mongo.db.quotes.find(
        {"Author": Author}).skip(skips).limit(limit)
    # limit pages to match total documents
    final_page = math.ceil(
        (mongo.db.quotes.count_documents({"Author": Author}))/(limit))
    pages = range(1, int(final_page + 1))
    # Fail safe for if Author has no Categories key
    try:
        # Extract Categories from Authors object
        Categories = mongo.db.authors.find_one(
            {"Author": Author})["Categories"]
    # if no Categories key, return empty key
    except KeyError:
        Categories = []
    # return 6 similar authors whick match this authors category
    similar_authors = mongo.db.authors.find(
        {"Categories": {"$in":  Categories}}).limit(6)
    # Fail safe for if user is logged out
    try:
        # if user logged in
        if session["user"]:
            # get array of id's for users favourite quotes
            fav_quotes2 = get_starred(session["user"], "quote")
            # get array of id's for users favourite authors
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


# Function to get books
@app.route("/get_books", methods=["GET"])
def get_books():
    # identify is user requested saved favourites
    get_fav = request.args.get('get_fav')
    # Return batch of 30 books for user
    books = mongo.db.books.find().limit(30)
    # Fail safe for if user is logged out
    try:
        # if user logged in
        if session["user"]:
            # get array of id's to use for returning objects
            fav_books1 = get_favourites(session["user"], "book")
            # get list of favourite to identify which books to show as already favourited
            fav_books2 = get_starred(session["user"], "book")
            # if user has favourites saved and they requested to view them
            if fav_books1 and get_fav != "No":
                # update the books and pages with users favourites
                fav_books = mongo.db.books.find(
                    {"_id": {"$in":  fav_books1}}).limit(30)
                # update the books documents with favourites
                books = fav_books
    # if session["user"] not recognised, user is logged out
    except KeyError:
        # return fav_books2 as empty
        fav_books2 = []
    return render_template("books.html",
                           books=books,
                           fav_books2=fav_books2,
                           get_fav=get_fav)


# Function to search books
@app.route("/search_books", methods=["GET", "POST"])
def search_books():
    # if search function just activated
    generated = request.args.get('generated')
    if generated == "yes":
        # extract search query from form
        searchTerm = request.form.get("query_book")
    # For different pages extract query from url
    else:
        searchTerm = request.args.get('query_book')
    # Return results based on search and limit to 30
    books = mongo.db.books.find({"$text": {"$search": searchTerm}}).limit(30)
    # if search has been completed
    searched = True
    # Fail safe for if user is logged out
    try:
        # if user logged in
        if session["user"]:
            # get array of id's for users favourite quotes
            starred = get_starred(session["user"], "book")
    # if session["user"] not recognised, user is logged out
    except KeyError:
        starred = []
    return render_template('books.html',
                           books=books,
                           fav_books2=starred,
                           query_book=searchTerm,
                           searched=searched)


# function for individual Book profile
@app.route("/book_profile/<Book>", methods=["GET", "POST"])
def book_profile(Book):
    # limit book quotes to 6 results
    limit = int(6)
    # Get book quotes page number from url
    page = request.args.get('page', 1, type=int)
    # iterate through objects depending on page number
    skips = limit * (page - 1)
    # Locate book object
    book = mongo.db.books.find_one({"Book": Book})
    # set of book quotes to return
    quotes = mongo.db.quotes.find({"Book": Book}).skip(skips).limit(limit)
    # limit pages to match total documents
    final_page = math.ceil(
        (mongo.db.quotes.count_documents({"Book": Book}))/(limit))
    pages = range(1, int(final_page + 1))
    # Locate book Author
    author = mongo.db.books.find_one({"Book": Book})["Author"]
    # return all of authors books
    authors_books = mongo.db.authors.find_one({"Author": author})["Books"]
    # Fail safe for if user is logged out
    try:
        # if user logged in
        if session["user"]:
            # get array of id's for users favourite quotes
            fav_quotes2 = get_starred(session["user"], "quote")
            # get array of id's for users favourite books
            fav_books2 = get_starred(session["user"], "book")
    # if session["user"] not recognised, user is logged out
    except KeyError:
        fav_quotes2 = []
        fav_books2 = []
    return render_template("indiv_book.html",
                           book=book,
                           quotes=quotes,
                           authors_books=authors_books,
                           fav_quotes2=fav_quotes2,
                           fav_books2=fav_books2,
                           page=page,
                           pages=pages,
                           limit=limit,
                           final_page=final_page
                           )


# Funciton for mood page
@app.route("/get_mood")
def get_mood():
    return render_template("mood.html")


# Funciton for when mood form activated
@app.route("/generate_mood", methods=["GET", "POST"])
def generate_mood():
    # get page number
    page = request.args.get('page', 1, type=int)
    # limit quotes to 5 results
    limit = int(5)
    # iterate through objects depending on page number
    skips = limit * (page - 1)
    # identify if form initialised
    generated = request.args.get('generated')
    # if form initialised get list from form
    if generated == "yes":
        # Get searched tags from form
        search_tags = request.form.getlist('mood-button')
    # if form on next pages pass previously initialised tags
    else:
        # Get searched tags from url instead
        search_tags = request.args.getlist('search_tags')
    # limit results to 10 pages as results excessive
    final_page = 10
    pages = range(1, int(final_page + 1))
    # set of quotes to return
    quotes = mongo.db.quotes.find(
        {"$text": {"$search": str(search_tags)}}).skip(skips).limit(limit)
    # if form has been completed
    generated = True
    # Fail safe for if user is logged out
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
                           search_tags=search_tags
                           )


# Funciton for shared quote page
@app.route("/share_quote/<_id>", methods=["GET", "POST"])
def share_quote(_id):
    # Locate quote based on object ID
    quote = mongo.db.quotes.find_one({"_id": ObjectId(_id)})
    return render_template("share_quote.html",
                           quote=quote)


# Funciton for user to register
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


# Funciton for user to login
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


# Funciton for users profile page
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    user = mongo.db.users.find_one(
        {"username": session["user"]})
    # set of users favourite quotes to return
    fav_quotes1 = get_favourites(session["user"], "quote")
    quotes = mongo.db.quotes.find({"_id": {"$in":  fav_quotes1}})
    fav_quotes2 = get_starred(session["user"], "quote")
    # set of users favourite authors to return
    fav_authors1 = get_favourites(session["user"], "author")
    authors = mongo.db.authors.find({"_id": {"$in":  fav_authors1}})
    fav_authors2 = get_starred(session["user"], "author")
    # set of users favourite books to return
    fav_books = get_favourites(session["user"], "book")
    books = mongo.db.books.find({"_id": {"$in":  fav_books}})
    # if user logged in
    if session["user"]:
        return render_template("profile.html",
                               user=user,
                               quotes=quotes,
                               fav_quotes2=fav_quotes2,
                               authors=authors,
                               fav_authors2=fav_authors2,
                               books=books)

    return redirect(url_for("login"))


# funciton for comments section
@app.route("/comment", methods=["GET", "POST"])
def comment():
    if request.method == "POST":
        username = session["user"]
        # Get comment tect from form
        comment = request.form.get("comment")
        # which page the comment is from
        section = request.args.get('section')
        # The comment date
        today = datetime.today()
        date = today.strftime("%d/%m/%Y")
        # if from authors section
        if section == "authors":
            # Locate the authors object
            Author = request.args.get('Author')
            # Update with users comments details
            mongo.db.authors.update_one({"Author": Author}, {"$addToSet": {"Comments": {
                                        'text': comment, 'user': username, 'date': date}}})
            return redirect(url_for("author_profile", Author=Author))
        # if from books section
        if section == "books":
            # Locate the book object
            Book = request.args.get('Book')
            # Update with users comments details
            mongo.db.books.update_one({"Book": Book}, {"$addToSet": {"Comments": {
                                      'text': comment, 'user': username, 'date': date}}})
            return redirect(url_for("book_profile", Book=Book))


# Funciton for user to log out
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
