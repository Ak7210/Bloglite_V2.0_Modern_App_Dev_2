from . import api
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from applications.models.userdb import User
# from applications.models.searchdb import Searchuser

@api.route('/bloglite/search/<string:username>', methods=["GET"])
@jwt_required()
def search(username):

    results = User.query.filter(User.userUsername.like('%'+username + '%')).all()
    # print(results)
    if results:
        result = {'username' : []}
        for user in results:
            result['username'].append(user.userUsername)
        result['username'].sort()
        return jsonify(result), 200
    else:
        return jsonify({'msg' : 'No results found'}), 404


# use the api which is already created for the profileApi page.