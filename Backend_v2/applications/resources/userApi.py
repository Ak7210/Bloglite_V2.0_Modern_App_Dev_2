from . import api
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from applications.models.userdb import User, db
from flask_jwt_extended import get_jwt_identity, jwt_required,unset_jwt_cookies
from applications.resources.callablefunctions import checkPassword, checkUsername
from applications.resources.callablefunctions import userto_json
import os # it is used to create the folder
import shutil # it deletes the folder and all the files inside the folder

# blog_folder = 'applications/static/blogImages'
# profile_folder = 'applications/static/profileImages'

@api.route('/bloglite/user', methods=['GET'])
@jwt_required()
def getUser():
    currentUserId = get_jwt_identity()
    user = User.query.filter_by(userId = currentUserId).first()
    if user:
        userData = userto_json(user)
        return jsonify({
                        "user" : userData,
                        "msg": "User data send successfully"
                    }), 200
    else:
        return jsonify({'msg': 'User not found'}), 404

@api.route('/bloglite/user/report', methods=['PUT'])
@jwt_required()
def reportUser():
    currentUserId = get_jwt_identity()
    user = User.query.filter_by(userId = currentUserId).first()
    data = request.get_json()
    report = data['reportFormat'].strip()
    if user:
        if(user.monthlyReport == report):
            return jsonify({'msg': 'Report format already set'}), 409
        else:
            user.monthlyReport = report
            db.session.commit()
            return jsonify({
                            "msg": "Your monthly report format changed successfully"
                        }), 200

    else:
        return jsonify({'msg': 'User not found'}), 404



# New registraion Api
@api.route('/bloglite/registration', methods=['POST'])
def registration():
    registraionData = request.get_json()
    userName = registraionData['name'].strip()
    userUsername = registraionData['username'].strip()
    userPwd = registraionData['password'].strip()
    # condition check for username, if username is already present in database return choose another name.
    # if userUsername not in [None, ""] and userName not in [None, ''] and userPwd not in [None, '']:
    if checkUsername(userUsername) and checkPassword(userPwd):
        user = User.query.filter_by(userUsername = userUsername).first()         
        if not user:
            newUser = User(userName= userName,
                           userUsername=userUsername,
                           userPwd = generate_password_hash(userPwd)
                        )
            
            db.session.add(newUser)
            db.session.commit()

            return jsonify({'msg': 'Account Created Successfully'}), 201
        
        else:
            return jsonify({'msg' : 'Username already exits choose another username'}), 409
        
        # this section create the folder for the each new user
        # if userCreation(user):
        #     blog_path = os.path.join(blog_folder, userUsername)
        #     profile_path = os.path.join(profile_folder, userUsername)
        #     if not os.path.exists(blog_path):
        #         os.mkdir(blog_path)
        #     if not os.path.exists(profile_path):
        #         os.mkdir(profile_path)
        #     return jsonify({'msg': 'Account Created Successfully'}), 201
            
        # else:
        #     return jsonify({'msg' : 'Username already exits choose another username'}), 409 
         
    else:
        return jsonify({'msg': 'Please provide valid inputs'}), 400


# Password Api updation
@api.route('/bloglite/password_update', methods=['PUT'])
@jwt_required()
def passwordUpdate():
    userid = get_jwt_identity()
    passwordUpdate = request.get_json()
    oldPassword = passwordUpdate['oldpassword'].strip()
    newPassword = passwordUpdate['newpassword'].strip()
    user = User.query.get(userid)
    print(user)
    if user:
        if check_password_hash(user.userPwd, oldPassword) and checkPassword(newPassword):
            user.userPwd = generate_password_hash(newPassword)
            db.session.commit()

        # return redirect(url_for("api.logout")) # currently this is not working but the password is updating and the jwt_authentication is alwo working perfectly

            return jsonify({'msg': "password updated successfully"}), 200 #
        else:
            return jsonify({'msg': 'invalid password'}), 400
    else:
        return jsonify({'msg': 'Invalid credential'}), 400
    
# After updateting the password we have to remove the authentication token from header as well as local storage and also logout the user.


# Profile pic updation Api
# @api.route('/bloglite/propicupdate' ,methods=['PUT'])
# @jwt_required()
# def userUpdate():
#     currentUserId = get_jwt_identity()
#     pass


# profile name updation Api
# @api.route('/bloglite/nameupdate', methods=['PUT'])
# @jwt_required()
# def nameupdate():
#     currentUserId = get_jwt_identity()
#     user = User.query.get(currentUserId)
#     nameUpdate = request.get_json()
#     userName = nameUpdate['name'].strip()
#     if user:
#         user.userName = userName
#         db.session.commit()
#         return jsonify({'msg': 'Profile name updated successsfully'}), 200
#     else:
#         return jsonify({'msg': 'User not found'}), 404


# Delete the User from Database
@api.route('/bloglite/deleteuser', methods=['DELETE'])
@jwt_required()
def userDelete():
    currentUserId = get_jwt_identity()
    user = User.query.get(currentUserId)
    # userUsername = user.userUsername
    def userDelete(user):
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        else:
            return False
    if userDelete(user):
        # shutil.rmtree(os.path.join(profile_folder, userUsername))
        # shutil.rmtree(os.path.join(blog_folder, userUsername))
        return jsonify({'msg': 'User deleted successfully'}), 200
    else:
        return jsonify({'msg': 'Something went wrong'}), 400

#  All api for user worked very well






  



