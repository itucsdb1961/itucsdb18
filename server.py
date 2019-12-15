url = "postgres://vzvhmhqevlcedf:141b03607dee6c5c995d91b952b06e4fc122006f5cd2c1d789403aae34dc40a1@ec2-54-217-225-16.eu-west-1.compute.amazonaws.com:5432/dafo7esm4hjfc7"
secret_key = "hjkalsfdlamfrqwrxzc"

from flask import Flask, request, redirect, url_for, session
import os
import psycopg2 as dbapi2
#from views import home_page
#import author_view, book_view, closet_view, student_view

app = Flask(__name__)

def home_page():
	return "test"

def create_app():

	app.config.from_object("settings")

	app.add_url_rule("/", view_func=home_page)
	return app
	
'''
	app.add_url_rule("/admin/books", view_func = book_view.admin_books_page , methods=["GET", "POST"])

	app.add_url_rule("/books", view_func = book_view.books_page , methods=["GET", "POST"])
	app.add_url_rule("/book/<book_id>", view_func = book_view.book_page)
	app.add_url_rule("/book/delete/<book_id>", view_func = book_view.delete_book)

	app.add_url_rule("/author/<author_id>", view_func = author_view.author_page)
	app.add_url_rule("/author/delete/<author_id>", view_func = author_view.delete_author)

	app.add_url_rule("/admin/authors", view_func = author_view.admin_authors_page)
	app.add_url_rule("/authors", view_func = author_view.authors_page, methods=["GET", "POST"])

	app.add_url_rule("/admin/closets", view_func = closet_view.admin_closets_page, methods=["GET", "POST"])
	app.add_url_rule("/closets", view_func = closet_view.closets_page, methods=["GET", "POST"])


	app.add_url_rule("/login", view_func=views.admin_login_page, methods=["GET", "POST"])
	app.add_url_rule("/signup", view_func=views.admin_signup_page, methods=["GET", "POST"])
	app.add_url_rule("/logged", view_func=views.admin_logged_page, methods=["GET", "POST"])
	
	app.add_url_rule("/admin/students", view_func=student_view.admin_students, methods=["GET", "POST"])
	app.add_url_rule("/admin/student/<student_id>", view_func=student_view.admin_student, methods=["GET", "POST"])
'''
	

if __name__ == "__main__":
	
	create_app()
	port = app.config.get("PORT", 5000)

	app.run(host="0.0.0.0", port=port)
