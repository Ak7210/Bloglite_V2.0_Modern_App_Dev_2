from applications.models import db
from applications.models.userdb import User
# from applications.models.commentsdb import Comments
from applications.models.blogdb import Blog
from applications.resources import api
from flask import request, jsonify, send_file
from flask_jwt_extended import get_jwt_identity, jwt_required
import os
import uuid
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route('/bloglite/blog/image', methods=['POST'])
@jwt_required()
def uploadImage():
    currentUserId = get_jwt_identity()
    user = User.query.filter_by(userId = currentUserId).first()
    # path = os.path.join('./applications/static/blogImages', user.userUsername)
    
    path = './applications/static/blogImages' #Change the Shiva123 to the username of the current user

    if 'files' not in request.files: # file is the name of the input field it is available in vuejs
        # print('no files')
        return jsonify({'msg': 'no files'}), 400
    files = request.files.getlist('files')   # file is the name of the input field it is available in vuejs and update it for multiple files

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            name_image = str(uuid.uuid4()) + filename
            imagepath = os.path.join(path, name_image)
            file.save(imagepath)
            # print(imagepath)
            return jsonify({'msg': 'image uploaded successfully', 'imageUrl': name_image}), 200
        else:
            return jsonify({'msg': 'image not uploaded succesfully please try again'}), 400
        
@api.route('/image/<string:filename>', methods=['GET'])
def get_image(filename):
     path = './static/blogImages'
     imagepath = os.path.join(path, filename)
    #  print(imagepath)
     return send_file(imagepath)
    
    
        