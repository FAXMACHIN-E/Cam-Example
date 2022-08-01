from flask_sqlalchemy import SQLAlchemy
from datetime import datetime # get dates & times

Db = SQLAlchemy()


class User(Db.Model):
    __tablename__ = 'users'
    uid = Db.Column(Db.Integer, primary_key=True, autoincrement=True)
    username = Db.Column(Db.String(64), unique=True, nullable=False)
    password = Db.Column(Db.String(128), nullable=False) # Note the max length of password
    date_registered = Db.Column( Db.DateTime, nullable = True, default = datetime.now() )


class File(Db.Model):
    __tablename__ = 'files'
    file_id = Db.Column(Db.Integer, primary_key=True, autoincrement=True)
    uploader = Db.Column(Db.Integer, Db.ForeignKey('users.uid'), nullable=False)
    # user = Db.relationship('User', backref='post')
    letter = Db.Column(Db.String(1024), nullable=False) # Note the max length of a string
    # likes = Db.Column(Db.Integer, default=0)
    date_created    = Db.Column( Db.DateTime, nullable = True, default = datetime.now() )

class Blab(Db.Model):
    __tablename__ = 'blabs'
    blab_id = Db.Column(Db.Integer, primary_key=True, autoincrement=True)
    author = Db.Column(Db.Integer, Db.ForeignKey('users.uid'), nullable=False)
    user = Db.relationship('User', backref='post')
    content = Db.Column(Db.String(1024), nullable=False) # Note the max length of a string
    likes = Db.Column(Db.Integer, default=0)
    date_created    = Db.Column( Db.DateTime, nullable = True, default = datetime.now() )
