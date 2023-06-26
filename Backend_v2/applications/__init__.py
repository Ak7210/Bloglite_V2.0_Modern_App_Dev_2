from flask import Flask
from applications.cache import cache #cache is an instance of Cache class

from applications.resources import jwt, api 
from flask_cors import CORS

from applications.models import db
from applications.resources.userApi import *
from applications.resources.authenticationApi import *
from applications.resources.commentApi import *
from applications.resources.relationsApi import *
from applications.resources.searchApi import *
from applications.resources.feedsApi import *
from applications.resources.profileApi import *
from applications.resources.imageApi import *
from applications.resources.blogcreate import *
from applications.resources.exportApi import *
from applications.resources.summaryApi import *
from applications.resources.likes_dislikesApi import *
from applications import jobs



def create_app(config):
    app = Flask(__name__)
    jwt.init_app(app)      
    CORS(app)
    app.config.from_object(config)
    db.init_app(app)
    cache.init_app(app)
    app.app_context().push()
    app.register_blueprint(api)
    celery = jobs.celery
    celery.Task = jobs.ContextTask
    return app, celery