from datetime import timedelta

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database/bloglite.sqlite3'
    SECRET_KEY = 'agdrwedgffsfqtewadsfgfhar1254@'
    JWT_SECRET_KEY = 'This is a top secret key'
    JWT_COOKIE_SECURE = True # in production this should always be set true
    WTF_CSRF_ENABLED = False # It is used for server side form authentication
    JWT_TOKEN_LOCATION = ['headers', "cookies"] # Location of the token 
    JWT_ACCESS_COOKIE_NAME = 'access_token' # Name of the cookie
    JWT_ACCESS_TOKEN_EXPIRES  = timedelta(days=1) # Token expiration time




