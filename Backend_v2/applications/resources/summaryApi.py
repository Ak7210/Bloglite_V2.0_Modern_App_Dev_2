from . import api
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from applications.models.userdb import User
from applications.models.blogdb import Blog
from applications.models.commentsdb import Comments

#  get the blog details
@api.route('/bloglite/summary', methods=['GET'])
@jwt_required()
def summary():
    userId = get_jwt_identity()
    user = User.query.get(userId)
    if user:
        blogs = Blog.query.filter_by(blogUserId = user.userId).all()

        user_comments = Comments.query.filter_by(commentPostby = user.userId).all()
        comments_on_blog = []
        # day_vs_total_comm = {}
        for blog in blogs:
            comments_on_blogs = Comments.query.filter_by(commentBlogId = blog.blogId).all()
            comments_on_blog.append((blog.blogTitle, len(comments_on_blogs), blog.likes, blog.dislikes))
            # for comment in comments_on_blogs:
            #     if comment.commentTime in day_vs_total_comm:
            #         day_vs_total_comm[comment.commentTime.strftime( "%b %d %Y")] += 1
            #     else:
            #         day_vs_total_comm[comment.commentTime.strftime("%b %d %Y")] = 1

        
        summary_data = {

            'user': user.userName,"number_of_followers":user.userNoFollowers,
            "number_of_followings": user.userNoFollowing, 'number_blogs_created': len(blogs),
            'users_comment': len(user_comments), 'comment_on_blogs': comments_on_blog,

        }
        # print(summary_data)
        
        return jsonify(summary_data), 200
    else:
        return jsonify({'msg': 'User not found'}), 404

        