import os
import sys
from flask import Flask
from flask_restx import Api
from flask_cors import CORS

api_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
src_path = os.path.abspath(os.path.join(api_path, os.path.pardir))
lib_path = os.path.abspath(os.path.join(src_path, 'lib'))
if api_path not in sys.path:
    sys.path.append(api_path)
if lib_path not in sys.path:
    sys.path.append(lib_path)

# Module
from lib.encrypt import EncryptManager
from lib.db_connect import MySQLManager, RDSManager
from lib.validator import ApiValidator
EncryptManager = EncryptManager()
MySQLManager = MySQLManager()
RDSManager = RDSManager()
ApiValidator = ApiValidator()


def create_app():
    app = Flask(__name__)
    # Swagger namespace
    from . import user
    api = Api(app, title="User login", doc="/doc")
    api.add_namespace(user.user_namespace, path="/user")
    
    CORS(app=app, resources={r"/user/*": {"origins": "*"},
                             r"/auth/*": {"origins": "*"},
                             r"/doc/*": {"origins": "*"}})
    return app
