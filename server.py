from flask import Flask

import views

app = Flask(__name__)

def create_app():

	app.config.from_object("settings")

	app.add_url_rule("/", view_func=views.home_page)
	app.add_url_rule("/books", view_func=views.books_page)
	app.add_url_rule("/movies", view_func=views.authors_page)
	app.add_url_rule("/movies", view_func=views.closets_page)
	app.add_url_rule("/movies", view_func=views.admin_login_page)

	return app

if __name__ == "__main__":

	create_app()
	port = app.config.get("PORT", 5000)
	app.run(host="0.0.0.0", port=port)






