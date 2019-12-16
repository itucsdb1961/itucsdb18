url = "postgres://mrzogiikkbrxmf:b6042668a00f9ea7e4d353f06e02e8c5ffab90a6a2a76191de8597340a254d68@ec2-54-228-243-29.eu-west-1.compute.amazonaws.com:5432/dsbe8b5jahoaq"
secret_key = "hjkalsfdlamfrqwrxzc"

from flask import Flask, request, redirect, url_for, session
import os
import psycopg2 as dbapi2
import views
import author_view, book_view, closet_view, student_view, shelf_view

app = Flask(__name__)

app.config.from_object("settings")

app.add_url_rule("/", view_func=views.home_page, methods=["GET", "POST"])
app.add_url_rule("/admin/books", view_func = book_view.admin_books_page , methods=["GET", "POST"])

app.add_url_rule("/books", view_func = book_view.books_page , methods=["GET", "POST"])

app.add_url_rule("/book/<book_id>", view_func = book_view.book_page, methods=["GET", "POST"])

app.add_url_rule("/author/<author_id>", view_func = author_view.author_page, methods=["GET", "POST"])

app.add_url_rule("/admin/authors", view_func = author_view.admin_authors_page, methods=["GET", "POST"])
app.add_url_rule("/authors", view_func = author_view.authors_page, methods=["GET", "POST"])

app.add_url_rule("/admin/closets", view_func = closet_view.admin_closets_page, methods=["GET", "POST"])
app.add_url_rule("/closets", view_func = closet_view.closets_page, methods=["GET", "POST"])
app.add_url_rule("/closet/<closet_id>", view_func = closet_view.closet_page, methods=["GET", "POST"])

app.add_url_rule("/login", view_func=views.admin_login_page, methods=["GET", "POST"])
app.add_url_rule("/signup", view_func=views.admin_signup_page, methods=["GET", "POST"])
app.add_url_rule("/logged", view_func=views.admin_logged_page, methods=["GET", "POST"])
app.add_url_rule("/logged_out", view_func=views.admin_logout_page)

app.add_url_rule("/admin/students", view_func=student_view.admin_students, methods=["GET", "POST"])
app.add_url_rule("/admin/student/<student_id>", view_func=student_view.admin_student, methods=["GET", "POST"])

app.add_url_rule("/admin/shelves", view_func=shelf_view.admin_shelves_page, methods=["GET", "POST"])
app.add_url_rule("/shelve/<shelf_id>", view_func = shelf_view.shelf_page, methods=["GET", "POST"])

port = app.config.get("PORT", 5000)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=port)
