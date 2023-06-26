from . import api
from flask import request, jsonify
from datetime import datetime
from applications.models import db
from applications.models.blogdb import Blog
from applications.models.userdb import User

from applications.resources.callablefunctions import blogto_json
from flask_jwt_extended import get_jwt_identity, jwt_required



# Creating a new Blog
@api.route('/bloglite/blog', methods=['POST'])
@jwt_required()
def createblog():
    currentUserId = get_jwt_identity()
    blogData = request.get_json()
    blogTitle = blogData['blogTitle'].strip()
    blogCaption = blogData['caption'].strip()
    blogImageURL = blogData['imageUrl'] # I think it is not a good way to handle the json formated image. think about it before implemented
    blogArchive = blogData['isArchived']
    user = User.query.filter_by(userId = currentUserId).first() # used only for the foreignKey also we can user here jwt_token authentication.
    if user:
        if blogTitle not in [None, '']:
            if blogArchive == True:
                newBlog = Blog(
                            blogTitle = blogTitle,
                            blogCaption = blogCaption,
                            blogArchive = True,
                            blogImageURL = blogImageURL,
                            blogUserId = user.userId,
                            blogCreation = datetime.now()
                        )

                db.session.add(newBlog)
                user.userNoBlog += 1
                db.session.commit()
                newBlog = blogto_json(newBlog)
                newBlog["comments"] = []
                return jsonify({"msg": 'Blog created successfully', "blog": newBlog }), 201
            else:
                newBlog = Blog(
                            blogTitle = blogTitle,
                            blogCaption = blogCaption,
                            blogImageURL = blogImageURL,
                            blogUserId = user.userId,
                            blogCreation = datetime.now()
                        )
                
                db.session.add(newBlog)
                user.userNoBlog += 1
                db.session.commit()
                newBlog = blogto_json(newBlog)
                newBlog["comments"] = []
                # print(newBlog)
                return jsonify({'msg': 'Blog created successfully', "blog": newBlog}), 201
        else:
            return jsonify({'msg': 'Invalid input'}), 400



# updateting the particular blog
@api.route('/bloglite/blog/<int:blogid>', methods=['PUT'])
@jwt_required()
def updateblog(blogid):
    currentUserId = get_jwt_identity()
    updateBlog = request.get_json()
    blogTitle = updateBlog['blogTitle'].strip()
    blogCaption = updateBlog['caption'].strip()
    blogImageURL = updateBlog['imageUrl'] # I think it is not a good way to handle the json formated image. think about it before implemented
    blogArchive = updateBlog['isArchived']
    deleteImg = updateBlog['deleteImg']
    oldBlog = Blog.query.filter_by(blogId = blogid, blogUserId = currentUserId).first()
    if oldBlog:
        count = 0
        if blogTitle not in [None, '']:
            oldBlog.blogTitle = blogTitle
            count += 1

        if blogArchive == "private":
            oldBlog.blogArchive = True
            count += 1

        if blogArchive == "public":
            oldBlog.blogArchive = False
            count += 1

        if blogCaption not in [None, '']:
            oldBlog.blogCaption = blogCaption
            count += 1

        if blogImageURL not in [None, ''] and deleteImg in [False, 'false', 'False']:
            oldBlog.blogImageURL = blogImageURL
            count += 1
        if blogImageURL in [None, ''] and deleteImg in [True, 'true', 'True']:
            oldBlog.blogImageURL = None
            count += 1
        if blogImageURL not in [None, ''] and deleteImg in [True, 'true', 'True']:
            return jsonify({'msg': 'Invalid input'}), 400
            
        if deleteImg in [True, 'true', 'True']:
            oldBlog.blogImageURL = None
            count += 1

# one more situation may be arise here.... if user already updated the image and now they want to remove the image..... then we should have to handle this sitution in backend.

        if count > 0:
            oldBlog.blogCreation = datetime.now()
            db.session.commit()
            # print(blogto_json(oldBlog))
            return jsonify({'msg' : 'Blog data updated successfully',  "updateblog": blogto_json(oldBlog)}), 200
        else:
            return jsonify({'msg': 'Blog data not updated'}), 400
    else:
        return jsonify({'msg' : 'Blog not found'}), 404




# Deleting the particular blog
@api.route('/bloglite/blog/<int:blogid>', methods=['DELETE'])
@jwt_required()
def deleteblog(blogid):
    currentUserId = get_jwt_identity()
    user = User.query.get(currentUserId)
    blog = Blog.query.filter_by(blogId = blogid, blogUserId = currentUserId).first()
    if blog:
        db.session.delete(blog)
        user.userNoBlog -= 1
        db.session.commit()
        return jsonify({'msg': 'Blog deleted Successfully'}), 200
    else:
        return jsonify({'msg': 'Blog not fount'}), 404




