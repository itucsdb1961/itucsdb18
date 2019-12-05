from flask import Flask
import os
import views
import psycopg2 as dbapi2
from dbinit import init_db
from flask import request, redirect, url_for


url = "postgres://vzvhmhqevlcedf:141b03607dee6c5c995d91b952b06e4fc122006f5cd2c1d789403aae34dc40a1@ec2-54-217-225-16.eu-west-1.compute.amazonaws.com:5432/dafo7esm4hjfc7"
secret_key = "hjkalsfdlamfrqwrxzc"
app = Flask(__name__)

def create_app():

	app.config.from_object("settings")

	app.add_url_rule("/", view_func=views.home_page)
	
	app.add_url_rule("/books", view_func=views.books_page , methods=["GET", "POST"])
	app.add_url_rule("/book/<book_id>", view_func = views.book_page)
	app.add_url_rule("/book/delete/<book_id>", view_func = views.delete_book)


	app.add_url_rule("/authors", view_func=views.authors_page, methods=["GET", "POST"])
	app.add_url_rule("/author/<author_id>", view_func = views.author_page)
	app.add_url_rule("/author/delete/<author_id>", view_func = views.delete_author)


	app.add_url_rule("/closets", view_func=views.closets_page)

	app.add_url_rule("/book/<book_id>", view_func=views.book_page)


	app.add_url_rule("/authors", view_func=views.authors_page)
	app.add_url_rule("/closets", view_func=views.closets_page, methods=["GET", "POST"])
	app.add_url_rule("/login", view_func=views.admin_login_page)


	app.add_url_rule("/admin/books", view_func=views.admin_books_page , methods=["GET", "POST"])

	return app

if __name__ == "__main__":
	create_app()
	port = app.config.get("PORT", 5000)

	init_db(url)

	app.run(host="0.0.0.0", port=port)
