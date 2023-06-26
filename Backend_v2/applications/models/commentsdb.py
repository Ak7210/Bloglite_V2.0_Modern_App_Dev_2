from . import db
from datetime import datetime

class Comments(db.Model):
    commentId = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    commentTime = db.Column(db.DateTime, default= datetime.now(), nullable=False)
    commentPostby = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    commentBlogId = db.Column(db.Integer, db.ForeignKey('blog.blogId'), nullable=False)

