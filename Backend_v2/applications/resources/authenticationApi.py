from . import api
from applications.models.userdb import User, db
from werkzeug.security import check_password_hash
from flask import request, jsonify
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, unset_jwt_cookies


#  login Authentication
@api.route('/bloglite/login', methods=['POST'])
def login():
    loginData = request.get_json()
    userUsername = loginData['username'].strip()
    userPwd = loginData['password'].strip()
    user = User.query.filter_by(userUsername = userUsername).first()
    if user and check_password_hash(user.userPwd, userPwd):
        access_token = create_access_token(identity=user.userId)
        response = jsonify({"access_token": access_token, "msg": "Login successfully"})
        set_access_cookies(response, access_token)
        return response, 200
    else: 
        return jsonify({'msg': 'invalid credentials'}) , 404


#  logout the User and remove the token.
@api.route('/bloglite/logout', methods=['GET'])
@jwt_required()
def logout():
    logout = jsonify({'msg' : 'Logout successfully'})
    unset_jwt_cookies(logout)
    return logout, 200
