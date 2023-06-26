from . import db


class Relations(db.Model):
    relationId = db.Column(db.Integer, primary_key=True)
    followingId = db.Column(db.Integer,  nullable=False)
    followerId = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)

# For the following follower relationship we can count followerId for number of following and followingID for number of followers.
# Handle this condition carefully.