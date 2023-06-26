from . import api
from flask import jsonify, after_this_request, send_file
from applications.models.userdb import User
from applications.models.blogdb import Blog
from applications.jobs.exportjobs import export_blog_as_csv
from flask_jwt_extended import get_jwt_identity, jwt_required
from os import remove

@api.route("/export/blog/<int:blogId>", methods=["GET"])
@jwt_required()
def export_blog(blogId):
    blog = Blog.query.get(blogId)
    if blog:
        task = export_blog_as_csv.delay(blogId)
        return jsonify({"message": "exporting blog to csv", "taskID":task.id}), 200
    
    return jsonify({"message": "blog not found"}), 404

@api.route("/export/blog/status/<string:taskID>", methods=["GET"])
@jwt_required()
def export_blog_status(taskID):
    task = export_blog_as_csv.AsyncResult(taskID)
    return jsonify({"taskID": task.id, "status": task.status}), 200


@api.route("/bloglite/download/blog/<int:blogId>", methods=["GET"])
# @jwt_required()
def export_blog_download(blogId):
    blog = Blog.query.get(blogId)
    if blog is None:
        return jsonify({"message": "blog not found"}), 404
    
    @after_this_request
    def remove_file(response):
        try:
            remove("applications/static/exportCsv/download_blog_{}.csv".format(blogId))

        except Exception as error:
            print(error)
        return response
    return send_file("static/exportCsv/download_blog_{}.csv".format(blogId), as_attachment=True)

