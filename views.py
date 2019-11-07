from flask import Flask,render_template

from server import app

@app.route("/")
def home_page():
    return render_template("home.html")

@app.route("/books")
def books_page():
    return render_template("books.html")

@app.route("/")
def authors_page():
    return render_template("authors.html")

@app.route("/")
def closets_page():
    return render_template("closets.html")

@app.route("/")
def admin_login_page():
    return render_template("admin_login.html") 