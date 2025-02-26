#imports
from flask import Flask
from application.database import db
from application.resources import *
import os
from flask_restful import Api
api = Api()

app=None

def create_app():
    app=Flask(__name__)
    app.debug=True
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///gohappy.sqlite3"
    upload_folder='static/documents'
    app.config['UPLOAD_FOLDER']=upload_folder
    app.config['MAX_CONTENT_LENGTH']=5*1024*1024
    db.init_app(app)
    api.init_app(app)
    app.app_context().push()
    return app

app=create_app()

from application.controllers import *

if __name__ == "__main__":
    app.run()

