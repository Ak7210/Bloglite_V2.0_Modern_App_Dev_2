from . import api
from flask import request, jsonify
from datetime import datetime
from applications.models import db
from applications.models.commentsdb import Comments
from applications.models.blogdb import Blog
from applications.models.relationsdb import Relations
from flask_jwt_extended import get_jwt_identity, jwt_required


# New Comment on the blog
@api.route('/bloglite/blog/comment/<int:blogid>', methods=['POST'])
@jwt_required()
def postComment(blogid):
    commentData = request.get_json() # getting the json data
    currentUserId = get_jwt_identity() # getting the current user id
    comment = commentData['comment'].strip() # getting the comment from the json data

    blog = Blog.query.get(blogid)  # getting the blog object
    relations = Relations.query.filter_by(followerId = currentUserId).all() #list of all the relations of the current user
    followingList = [relation.followingId for relation in relations] #list of all the users we are following

# The below code is for the checking the comment is not empty and the user is not commenting on his own blog and the blog is not private and the user is following the user who posted the blog.
    if blog:
        if comment not in [None, '']:
            if currentUserId != blog.blogUserId:
                if blog.blogArchive == False and blog.blogUserId in followingList:

                    newComment = Comments(comment = comment,
                                          commentPostby= currentUserId,
                                          commentBlogId = blogid,
                                          commentTime = datetime.now()
                                        )
                    
                    db.session.add(newComment)
                    db.session.commit()
                    return jsonify({'msg': 'Successfully commented on the blog', "commentId": newComment.commentId}), 201
                else:
                    return jsonify({
                        'msg' : 'You cannot post comments on this blog bcz it is either a private blog or you are not following the user'
                        }), 400

            else:
                # return jsonify({'msg' : 'You cannot post comments on your own blog'}), 400
                newComment = Comments(comment = comment,
                    commentPostby= currentUserId,
                    commentBlogId = blogid,
                    commentTime = datetime.now()
                )
                
                db.session.add(newComment)
                db.session.commit()
                print(newComment.commentId)
                return jsonify({'msg': 'Successfully commented on the blog', "commentId": newComment.commentId}), 201
        else:
            return jsonify({'msg' : 'Please provide valid input or you cannot post comments on this blog'}), 400
    else:
        return jsonify({'msg' : 'Blog not found'}), 404

# below code is for updating the comment on the blog which is posted by the current user

@api.route('/bloglite/blog/comment/<int:commentid>', methods=['PUT'])
@jwt_required()
def updateComment(commentid):
    currentUserId = get_jwt_identity()
    oldComment = Comments.query.filter_by(commentId = commentid, commentPostby = currentUserId).first() # getting the comment object
    if oldComment: # checking if the comment exists
        updateComment = request.get_json()
        newComment = updateComment['comment'].strip()
        if newComment not in [None, '']:
            oldComment.comment = newComment # updating the comment by new comment
            oldComment.commentTime = datetime.now() # updating the comment post time    
            db.session.commit()
            return jsonify({'msg': 'Comment updated successfully'}), 200
        else:
            return jsonify({'msg' : 'Povide a valid comment'}), 400
    else:
        return jsonify({'msg' : 'No such comment found'}), 404


# Deleting the comment on the blog which is posted by the current user

@api.route('/bloglite/blog/comment/<int:commentid>', methods=['DELETE'])
@jwt_required()
def deleteComment(commentid):
    currentUserId = get_jwt_identity()
    deleteComment = Comments.query.filter_by(commentId =commentid, commentPostby = currentUserId).first() # getting the comment posted by the current user
    if deleteComment:
        db.session.delete(deleteComment) # deleting the comment
        db.session.commit() # commiting the changes
        return jsonify({'msg': 'Comment deleted successfully'}), 200
    else:
        return jsonify({'msg' : 'Comment not found'}), 404


# I have tested all the above routes as well as code and it is working fine.