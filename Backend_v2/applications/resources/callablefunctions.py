from time import mktime as epoch
# Convert the user object to dictionary
def userto_json(user):
    userDict = {}
    userDict["userId"] = user.userId
    userDict["userName"] = user.userName
    userDict["userUsername"] = user.userUsername
    # userDict["userImgURL"] = user.userImgURL
    userDict["userNoBlog"] = user.userNoBlog
    userDict["userNoFollowers"] = user.userNoFollowers
    userDict["userNoFollowing"] = user.userNoFollowing
    return userDict

def searchUser_json(user):
    userDict = {}
    userDict["userName"] = user.userName
    userDict["userUsername"] = user.userUsername
    # userDict["userImgURL"] = user.userImgURL
    userDict["userNoBlog"] = user.userNoBlog
    userDict["userNoFollowers"] = user.userNoFollowers
    userDict["userNoFollowing"] = user.userNoFollowing
    return userDict



# Convert the blog object to dictionary
def blogto_json(blog):
    blogDict = {}
    blogDict["blogId"] = blog.blogId
    blogDict["blogTitle"] = blog.blogTitle
    blogDict["blogCaption"] = blog.blogCaption
    blogDict['likes'] = blog.likes
    blogDict['dislikes'] = blog.dislikes
    blogDict["blogImageURL"] = blog.blogImageURL
    blogDict["blogArchive"] = blog.blogArchive
    blogDict["blogCreation"] = int(epoch(blog.blogCreation.timetuple())*1000)
    blogDict["blogUserId"] = blog.blogUserId     
    return blogDict


# Convert the comment object to dictionary
def commentto_json(comment):
    commentDict = {}
    commentDict["commentId"] = comment.commentId
    commentDict["comment"] = comment.comment
    commentDict["commentTime"] = int(epoch(comment.commentTime.timetuple())*1000)
    commentDict["commentPostby"] = comment.commentPostby
    commentDict["commentBlogId"] = comment.commentBlogId
    return commentDict

# check password strength
def checkPassword(password):
    if password in [None, '']:
        return False
    if len(password) < 8 or len(password) > 20:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char in "!@#$%^&*()_+" for char in password):
        return False
    if any(char.isspace() for char in password):
        return False
    return True

# check username
def checkUsername(username):
    if username in [None, '']:
        return False
    if len(username) < 4 or len(username) > 20:
        return False
    if any(char.isspace() for char in username):
        return False
    return True

# sorted blogs
def sort_blogs(posts):
    # Sort the list of posts based on the value of the 'datetime' key
    if(len(posts) >0):
        sorted_posts = sorted(posts, key=lambda post: post['blogCreation'], reverse=True)
        return sorted_posts
    else:
        return posts


# sorted comments
def sort_comments(comments):
    sorted_comments = sorted(comments, key=lambda comment: comment['commentTime'], reverse=True)

    return sorted_comments
