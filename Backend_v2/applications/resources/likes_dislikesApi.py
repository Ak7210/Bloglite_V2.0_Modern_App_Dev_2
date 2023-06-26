# api for likes and dislikes
from . import api
from applications.models import db
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from applications.models.userdb import User
from applications.models.blogdb import Blog
from applications.models.bloglikesdb import LikesDislikes

@api.route('/bloglite/blog/like/<int:blogId>', methods=["GET"])
@jwt_required()
def likes(blogId):
    blog = Blog.query.get(blogId)
    current_userId = get_jwt_identity()
    # print(blogId)
    if blog:
        # print(blog)
        likes_dislikes_data = LikesDislikes.query.filter_by(blogId = blogId).all()
        a = False
        b = ''
        if likes_dislikes_data:
            for data in likes_dislikes_data:
                if data.userId == current_userId:
                    a = True
                    b = data.like_dislike_Id
                    break
        
        if(a==True and b != ''):
            filtered_data = LikesDislikes.query.get(b)
            if(filtered_data and filtered_data.like == False and filtered_data.dislike == True):
                filtered_data.like = True
                filtered_data.dislike = False
                blog.likes += 1
                blog.dislikes -= 1
                db.session.commit()
                return jsonify({'msg': "You liked this blog", "id": 1}), 200
            
            if (filtered_data and filtered_data.like == True and filtered_data.dislike == False):
                return jsonify({'msg': "You have already liked this blog"}), 400
            
        if(a == False and b == ''):
            new_like = LikesDislikes(userId = current_userId,
                                     like = True,
                                     dislike = False,
                                     blogId = blogId
                                )
            
            db.session.add(new_like)
            blog.likes += 1
            db.session.commit()
            return jsonify({"msg": "You liked this blog", 'id': 0}), 200
    else:
        return jsonify({"msg": "Blog not found"}), 400

@api.route("/bloglite/blog/dislike/<int:blogId>", methods = ["GET"])
@jwt_required()
def dislike(blogId):
    # code for dislikes
    blog = Blog.query.get(blogId)
    current_userId = get_jwt_identity()
    # print(blog)
    if blog:
        likes_dislikes_data = LikesDislikes.query.filter_by(blogId = blogId).all()
        # print(likes_dislikes_data)
        a = False
        b = ''
        if likes_dislikes_data:
            for data in likes_dislikes_data:
                if data.userId == current_userId:
                    a = True
                    b = data.like_dislike_Id
                    break
        
        if(a==True and b != ''):
            filtered_data = LikesDislikes.query.get(b)
            # print(filtered_data)
            if(filtered_data and filtered_data.like == True and filtered_data.dislike == False):
                filtered_data.like = False
                filtered_data.dislike = True
                blog.likes -= 1
                blog.dislikes += 1
                db.session.commit()
                return jsonify({'msg': "You disliked this blog", "id": 1}), 200
            
            if (filtered_data and filtered_data.like == False and filtered_data.dislike == True):
                return jsonify({'msg': "You have already liked this blog"}), 400
        if(a == False and b == ''):
            new_dislike = LikesDislikes(userId = current_userId,
                                        like = False,
                                        dislike = True,
                                        blogId = blogId
                                    )
            
            db.session.add(new_dislike)
            blog.dislikes += 1
            db.session.commit()
            return jsonify({"msg": "You liked this blog", 'id': 0}), 200
    else:
        return jsonify({"msg": "Blog not found"}), 400


            

