from application import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(128), nullable = False)
    password = db.Column(db.String(128), nullable = False)
    fullname = db.Column(db.String(128), nullable = False)
    email = db.Column(db.String(128), nullable = False)
    profile_pic = db.Column(db.String(128), default="default.jpg")
    bio = db.Column(db.String(128))
    join_date = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())
    status = db.Column(db.Boolean(), default=True)

    follower_users = db.relationship("Relation", foreign_keys = "Relation.follower_id", backref = "follower", lazy=True)
    following_users = db.relationship("Relation", foreign_keys = "Relation.following_id", backref = "following", lazy=True)
    posts = db.relationship("Post", backref="post_owner", lazy=True)
    likes = db.relationship("Like", backref = "like_owner", lazy=True)
    comments = db.relationship("Comment", backref = "comment_owner", lazy=True)
    
class Relation(db.Model):
    __tablename__ = "relations"
    id = db.Column(db.Integer, primary_key = True)
    follower_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    following_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    status = db.Column(db.String(256), nullable = False)
    relation_date = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key = True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"),nullable = False)
    photo = db.Column(db.String(256), nullable = False)
    caption = db.Column(db.String(256), default="")
    status = db.Column(db.Boolean(), default=True)
    post_date = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())
    
    comments = db.relationship("Comment", backref="commented", lazy=True)
    likes = db.relationship("Like", backref="liked", lazy=True)

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key = True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable = False)
    commented_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    comment = db.Column(db.String(256), nullable = False)
    status = db.Column(db.Boolean(), default=True)
    comment_date = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())

class Like(db.Model):
    __tablename__ = "likes"
    id = db.Column(db.Integer, primary_key = True)
    like_count = db.Column(db.Integer, nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable = False)
    liked_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    like_date = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())