
from flask import Blueprint
from flask_jwt_extended import JWTManager
api = Blueprint("api", __name__)
jwt = JWTManager()