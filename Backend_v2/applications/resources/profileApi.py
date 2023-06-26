from . import api 
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from applications.models.userdb import User
from applications.models.relationsdb import Relations
from applications.models.blogdb import Blog
from applications.models.commentsdb import Comments
from applications.cache import cache
from applications.resources.callablefunctions import blogto_json, commentto_json, searchUser_json, sort_blogs, sort_comments



# We have to send the user profile data.
@api.route("/bloglite/profile/<string:username>", methods=["GET"])
@jwt_required()
# @cache.cached(timeout=360, key_prefix='profile')
def getProfile(username):
    # print(username)
    currentUserId = get_jwt_identity()
    user = User.query.filter_by(userUsername = username).first() #get the current user
    if user:
        if user.userId == currentUserId:
            blogs = Blog.query.filter_by(blogUserId = user.userId).all()
            # changes to be made
            userBlog = []

            if blogs:
                for blog in blogs:
                    comments = Comments.query.filter_by(commentBlogId = blog.blogId).all()
                    blogDict = blogto_json(blog)

                    blogDict['comments'] = []
                    if comments:
                        # if there are comments for the blog
                        for comment in comments:
                            # get the user who posted the comment
                            c_user = User.query.get(comment.commentPostby)
                            # get the comment in json format
                            commentDict = commentto_json(comment)
                            # add the username of the user who posted the comment
                            commentDict["c_userUsername"] = c_user.userUsername
                            # append the comment to the blog
                            blogDict["comments"].append(commentDict)
                        # sort the comments
                        blogDict["comments"] = sort_comments(blogDict["comments"])
                        
                    userBlog.append(blogDict)
        
        # feeds send the blogs, users and comments
            feeds = {}
            # sorting the blogs
            sorted_posts = sort_blogs(userBlog)
            # userBlog.sort(key = lambda x:x['blogCreation'])
            #final dala that we have to send
            feeds["blogs"] = sorted_posts

            # get the blogs of the user
            followersList = []
            followingList = []

            # get the followers of the user
            followers = Relations.query.filter_by(followingId = user.userId).all()
            if followers:
                for follower in followers:
                    followersList.append(follower.followerId)

            # get the following of the user
            following = Relations.query.filter_by(followerId = user.userId).all()
            if following:
                for follow in following:
                    followingList.append(follow.followingId)

            followerUser = []
            followingUser = []
            if followersList:
                for i in followersList:
                    foll_user = User.query.get(i)
                    followerUser.append({"user_id" : foll_user.userId, "username" : foll_user.userUsername})

            if followingList:
                for i in followingList:
                    foll_user = User.query.get(i)
                    followingUser.append({"user_id" : foll_user.userId, "username" : foll_user.userUsername})
            
            # get the feeds of the user

            # followerUser = followerUser.sort(key = lambda x:x['usernamer'])
            # followingUser = followingUser.sort(key = lambda x:x['username'])
            
            feeds["followers"] = followerUser
            feeds["following"] = followingUser


            # print(feeds)
            return jsonify(feeds), 200


        # if the user is not the current user
        elif user.userId != currentUserId:
            blogs = Blog.query.filter_by(blogUserId = user.userId).all()
            search_userBlog = []
            # changes to be made
            if blogs:
                
                for blog in blogs:
                    
                    if blog.blogArchive == False:
                        comments = Comments.query.filter_by(commentBlogId = blog.blogId).all()

                        blogDict = blogto_json(blog)

                        blogDict['comments'] = []
                        if comments:
                            # if there are comments for the blog
                            for comment in comments:
                                # get the user who posted the comment
                                c_user = User.query.get(comment.commentPostby)
                                # get the comment in json format
                                commentDict = commentto_json(comment)
                                # add the username of the user who posted the comment
                                commentDict["c_userUsername"] = c_user.userUsername
                                # append the comment to the blog
                                blogDict["comments"].append(commentDict)
                            # sort the comments
                            blogDict["comments"] = sort_comments(blogDict["comments"])
                            
                        search_userBlog.append(blogDict)
                    
        
        # feeds send the blogs, users and comments
            feeds = {}
            # sorting the blogs
            sorted_posts = sort_blogs(search_userBlog)
            # userBlog.sort(key = lambda x:x['blogCreation'])
            #final dala that we have to send
            feeds["blogs"] = sorted_posts
            feeds['userData'] = [searchUser_json(user)]

            # get the blogs of the user
            followersList = []
            followingList = []

            # get the followers of the user
            followers = Relations.query.filter_by(followingId = user.userId).all()
            if followers:
                for follower in followers:
                    followersList.append(follower.followerId)

            # get the following of the user
            following = Relations.query.filter_by(followerId = user.userId).all()
            if following:
                for follow in following:
                    followingList.append(follow.followingId)

            followerUser = []
            followingUser = []
            if followersList:
                for i in followersList:
                    foll_user = User.query.get(i)
                    followerUser.append({"user_id" : foll_user.userId, "username" : foll_user.userUsername})

            if followingList:
                for i in followingList:
                    foll_user = User.query.get(i)
                    followingUser.append({"user_id" : foll_user.userId, "username" : foll_user.userUsername})
            
            # get the feeds of the user

            # followerUser = followerUser.sort(key = lambda x:x['usernamer'])
            # followingUser = followingUser.sort(key = lambda x:x['username'])
            
            feeds["followers"] = followerUser
            feeds["following"] = followingUser
            return jsonify({"profile_feed" : feeds}), 200
    else:
        return jsonify({"message": "User not found"}), 404

