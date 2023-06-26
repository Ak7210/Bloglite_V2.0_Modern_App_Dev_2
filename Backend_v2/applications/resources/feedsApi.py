from . import api #import the api blueprint
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from applications.models.userdb import User, db
from applications.models.relationsdb import Relations
from applications.models.blogdb import Blog
from applications.models.commentsdb import Comments
from applications.resources.callablefunctions import blogto_json, commentto_json, sort_blogs, sort_comments
from applications.cache import cache


# Get the feeds of the current user
@api.route("/bloglite/feed", methods=["GET"])
@jwt_required()
# @cache.cached(timeout=30)
def getFeed():
    currentUserId = get_jwt_identity()
    user = User.query.get(currentUserId) #get the current user

    if user:
        relations = Relations.query.filter_by(followerId = currentUserId).all()
        followingList = [relation.followingId for relation in relations] #get the list of the users we are following
              

        # We have to get the following users blogs.
        followingUserblogs = []
        # blogIds = []
        for i in followingList:
            blogUser_i = Blog.query.filter_by(blogUserId = i).all() #get all the blogs of the users "i"
            f_user = User.query.get(i)
            
            if blogUser_i:

                for blog in blogUser_i:
                    comments = Comments.query.filter_by(commentBlogId = blog.blogId).all()
                    # print("printing the comments", comments)
                    if blog.blogArchive == False:
                        # blogIds.append(blog.blogId)
                        blogDict = blogto_json(blog)
                        blogDict["f_userUsername"] = f_user.userUsername
                        # making a commonet array for each blog
                        blogDict['comments'] = []
                        if comments:
                            # print("comments are there")
                            # if there are comments for the blog
                            for comment in comments:
                                # get the user who posted the comment
                                c_user = User.query.get(comment.commentPostby)
                                # get the comment in json format
                                commentDict = commentto_json(comment)
                                # add the username of the user who posted the comment
                                # print("commentDict", commentDict)
                                commentDict["c_userUsername"] = c_user.userUsername
                                # append the comment to the blog
                                blogDict['comments'].append(commentDict)
                        sorted_comment = sort_comments(blogDict["comments"])
                        blogDict["comments"] = sorted_comment                             
                        followingUserblogs.append(blogDict)
        
        # feeds send the blogs, users and comments
        feeds = {}
        sorted_posts = sort_blogs(followingUserblogs)
        #final dala that we have to send
        feeds["blogs"] = sorted_posts
        # For testing purpose
        # print(feeds)

        return jsonify({"feeds" : feeds}), 200
    else:
        return jsonify({"msg": "User not found"}), 404

       


        


        


