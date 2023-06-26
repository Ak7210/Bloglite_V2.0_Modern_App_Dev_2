from . import db


class LikesDislikes(db.Model):
    like_dislike_Id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    like = db.Column(db.Boolean)
    dislike = db.Column(db.Boolean)
    blogId = db.Column(db.Integer, db.ForeignKey('blog.blogId'), nullable=False)