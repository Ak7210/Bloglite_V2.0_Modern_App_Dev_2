from . import api
from applications.models.relationsdb import Relations, db
from applications.models.userdb import User
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required


@api.route('/bloglite/relation/<string:username>', methods=['POST'])
@jwt_required()
def follow(username):
    currentUserId = get_jwt_identity()
    # followingData = request.get_json()
    user = User.query.get(currentUserId)
    following_user = User.query.filter_by(userUsername = username).first()
    followingId = following_user.userId
    if user and user.userId != followingId: #check if user exists and if user is not following himself
        # check if the user is already following the user
        relation = Relations.query.filter_by(followerId = currentUserId, followingId = followingId).first()
        if relation:
            return jsonify({'msg': 'You are already following the user'}), 200
        
        new_following = Relations(followingId = followingId, followerId = user.userId) #create new relation
        db.session.add(new_following) #add relation to database

        # we have to increase the number of followers of the user we are following
        followingUser = User.query.get(followingId)
        followingUser.userNoFollowers += 1
        user.userNoFollowing += 1
        db.session.commit()
        return jsonify({'msg' : 'You are followign the user','id':0}), 200
    else:
        return jsonify({'msg': 'User not found', }), 404


@api.route('/bloglite/relation/<string:username>', methods=['DELETE'])
@jwt_required()
def unfollow(username):
    currentUserId = get_jwt_identity()

    following_user = User.query.filter_by(userUsername = username).first()

    currentUser = User.query.get(currentUserId) #get the current user
    followingId = following_user.userId
    relation = Relations.query.filter_by(followerId = currentUserId, followingId = followingId).first() #get the relation
    if relation:
        db.session.delete(relation)
        following_user.userNoFollowers -= 1 #decrement number of followers
        currentUser.userNoFollowing -= 1
        db.session.commit()
        return jsonify({'msg' : 'Person removed from following list', "id":0}), 200

    else:
        # return jsonify({'msg' : ''}), 200
        return jsonify({'msg' : 'You are not following the user' }), 200

# checked all the routes and they are working fine.
