url = "postgres://vzvhmhqevlcedf:141b03607dee6c5c995d91b952b06e4fc122006f5cd2c1d789403aae34dc40a1@ec2-54-217-225-16.eu-west-1.compute.amazonaws.com:5432/dafo7esm4hjfc7"
secret_key = "hjkalsfdlamfrqwrxzc"

from flask import Flask, request, redirect, url_for, session
import os
import psycopg2 as dbapi2
import views
import author_view, book_view, closet_view, student_view, shelf_view

app = Flask(__name__)

def create_app():



	app.config.from_object("settings")

	app.add_url_rule("/", view_func=views.home_page, methods=["GET", "POST"])
	app.add_url_rule("/admin/books", view_func = book_view.admin_books_page , methods=["GET", "POST"])

	app.add_url_rule("/books", view_func = book_view.books_page , methods=["GET", "POST"])

	app.add_url_rule("/book/<book_id>", view_func = book_view.book_page, methods=["GET", "POST"])
	app.add_url_rule("/book/delete/<book_id>", view_func = book_view.delete_book , methods=["GET", "POST"])

	app.add_url_rule("/author/<author_id>", view_func = author_view.author_page, methods=["GET", "POST"])
	app.add_url_rule("/author/delete/<author_id>", view_func = author_view.delete_author, methods=["GET", "POST"])

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

	return app

if __name__ == "__main__":

	create_app()
	port = app.config.get("PORT", 5000)

	app.run(host="0.0.0.0", port=port)
