from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, jsonify, request
from flask_cors import CORS
from flask_api import status
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required, get_jwt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import decode_token

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@raspberrypi5.local:3306/doko"
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///doko.db"
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
CORS(app)
jwt = JWTManager(app)

from doppelkopf import routes