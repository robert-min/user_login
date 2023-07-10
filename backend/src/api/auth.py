import jwt
from datetime import datetime, timedelta
from flask import request
from flask_restx import Namespace, Resource
from functools import wraps
from . import ApiValidator
from lib.utils import abort_repsonse
from lib.validator import UnAuthorizationError, BadRequestError
from lib.encrypt import EncryptManagerError
from lib.db_connect import MySQLManagerError, RDSManagerError

auth_namespace = Namespace("auth")

# TODO : TOKEN_KEY 환경변수로 수정
TOKEN_KEY = "fADAADSFVADF!@1231455AAA"

@auth_namespace.route("/login")
class UserLogin(Resource):
    def post(self):
        try:
            email = request.get_json()["email"]
            password = request.get_json()["password"]
            
            # Check api login validator.
            ApiValidator.check_login(email, password)

            token = jwt.encode({
                "email": email,
                "exp": datetime.utcnow() + timedelta(hours=2)
            }, TOKEN_KEY, algorithm="HS256")
            return {"status": "OK", "result": {"email": email, "token": token}}
        except UnAuthorizationError as e:
            return abort_repsonse(401, error=e)
        except (EncryptManagerError, MySQLManagerError, RDSManagerError) as e:
            return abort_repsonse(500, error=e, message=" Try again in a few minutes.")
        except Exception as e:
            return abort_repsonse(500, error=e, message=" Unknown error. Contact service manager.")
        

def login_required(func):
    @wraps(func)
    def check_login(*args, **kwargs):
        try:
            token = request.headers.get("Authorization")
            ApiValidator.check_token_existence(token)
            
            decode_token = jwt.decode(token, TOKEN_KEY, algorithms="HS256")
            ApiValidator.check_vaild_token_email(decode_token)
            return func(*args, **kwargs)
        except (BadRequestError, jwt.ExpiredSignatureError) as e:
            return abort_repsonse(400, error=e, message=" Please log in again.")
        except UnAuthorizationError as e:
            return abort_repsonse(401, error=e)
        except Exception as e:
            return abort_repsonse(500, e)
    return check_login
        