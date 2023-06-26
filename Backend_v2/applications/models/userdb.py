from . import db

class User(db.Model):
    userId = db.Column(db.Integer, primary_key = True)
    userName = db.Column(db.String(50), nullable=False)
    userUsername = db.Column(db.String(50), unique=True, nullable=False)
    userPwd = db.Column(db.String, nullable=False)
    monthlyReport = db.Column(db.String, default="pdf")
    userNoBlog = db.Column(db.Integer, default=0)
    userNoFollowers = db.Column(db.Integer, default=0)
    userNoFollowing = db.Column(db.Integer, default=0)
    userBlogs = db.relationship('Blog', backref ='user', cascade ="all, delete")
    userFollowing = db.relationship('Relations', backref='user', cascade="all, delete")
    userComments = db.relationship('Comments', backref='user', cascade="all, delete")
    userLikesDislikes = db.relationship('LikesDislikes', backref='user', cascade="all, delete")
 