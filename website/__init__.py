from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "databse.db"

# this function is called when app.py runs, and is returned. Lets you do some config bits here

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Post, Comment, Like

    with app.app_context():
        db.create_all()

    login_manager = LoginManager() #login_manager new instance of LoginManager class
    login_manager.login_view = "auth.login" # if the user isn't logged in, put them here
    login_manager.init_app(app)

    #decorator used to manage sessions?
    @login_manager.user_loader
    # function - pass id in to get user returned
    def load_user(id): #remember if we get this from an input it will be a string
        return User.query.get(int(id)) #hence the casting

    return app


# this used to be needed - flask now works with app context and creates an instance folder that contains the db (line 24/25)
# leaving it in just in case I ever follow a tutorial that includes it again
# def create_database(app):
#     if not path.exists("website/" + DB_NAME):
#         db.create_all(app=app)
#         print("created database")