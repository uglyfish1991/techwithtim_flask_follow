from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

# the class User inherits from the base class. A model is a table? 
# UserMixin is from flask_login

#includes one-to-many relationships - one user can have many posts, one post can have many comments
class User(db.Model, UserMixin):
    # the variable id is a column of a unique int, used to look up users
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(170), unique = True)
    username = db.Column(db.String(170), unique = True)
    password = db.Column(db.String(170))
    date_created = db.Column(db.DateTime(timezone = True),default = func.now())
    # any post which has the author as the id as the current user
    # back reference - from the post, how do I access the user object? add .user so I can write post.user rather than post.(the id) one user has many posts
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200),nullable=False)
    category = db.Column(db.String(200))
    text = db.Column(db.Text, nullable = False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    #foreign keys - even though it's lowercase, it's referencing the User table / class
    # when I delete the user that is referenced, delete all the posts too
    # without this, you can have posts assoiciated with deleted users
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Like', backref='post', passive_deletes=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)

# single table inheritance - different classes mapped to single table
# table of writeables - has all the columns needs for writeable things (posts and comments)
# will also have columns only for posts and comments - need to be nullable 

# descriminator column - type strong post maps to post, string comment maps to comment
# this is the one you should look at now

# LOOK 