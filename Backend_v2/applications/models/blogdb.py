from . import db
from datetime import datetime

class Blog(db.Model):
    blogId = db.Column(db.Integer, primary_key= True)
    blogTitle = db.Column(db.String, nullable=False)
    blogCaption = db.Column(db.String)
    blogImageURL = db.Column(db.String)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    blogArchive = db.Column(db.Boolean , default=False, nullable=False)
    blogCreation = db.Column(db.DateTime, nullable= False, default= datetime.now())
    blogUserId = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    userblogs = db.relationship('Comments', backref ='blog', cascade ="all, delete")
    userlikes = db.relationship('LikesDislikes', backref ='blog', cascade ="all, delete")

