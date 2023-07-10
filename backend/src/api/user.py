from flask_restx import Namespace, Resource
from flask import request
from . import EncryptManager, MySQLManager, RDSManager, ApiValidator
from .auth import login_required
from lib.encrypt import EncryptManagerError
from lib.db_connect import MySQLManagerError, RDSManagerError
from lib.validator import BadRequestError
from lib.utils import abort_repsonse

user_namespace = Namespace("user")


@user_namespace.route("/create")
class UserCreate(Resource):
    def post(self):
        """POST /user/create 
        ## Create user api.
        It receives email, name, and password as body values.
        For password encryption, the server generates a random dek. The password is encrypted with a dek.
        Email, name, and password are stored in user_auth table (MySQL) and dek are stored in user_dek (RDS).
        
        ## Body:
            email (str): user email
            name (str): user name
            password (str): user password
        
        ## Response:
            {"status": "OK", "result": result}
        """
        try:
            user_info = request.get_json()
            # Check api validator
            ApiValidator.check_user_input(user_info)
            ApiValidator.check_user_existence(user_info["email"])
            
            # Encrypt user password
            dek = EncryptManager.get_dek()
            user_info["password"] = EncryptManager.encrypt_password(dek, user_info["password"])
            
            # Insert user info in DB
            RDSManager.insert_user_dek(user_info["email"], dek)
            result = MySQLManager.insert_user_auth(user_info["email"], user_info["name"], user_info["password"])
            return {"status": "OK", "result": result}
        except BadRequestError as e:
            return abort_repsonse(400, error=e)
        except (EncryptManagerError, RDSManagerError) as e:
            return abort_repsonse(500, error=e, message=" Try again in a few minutes.")
        except MySQLManagerError as e:
            # Delete user DEK stored in RDS in case of MySQL DB error
            RDSManager.delete_user_dek(user_info["email"])
            return abort_repsonse(500, error=e, message=" Try again in a few minutes.")
        except Exception as e:
            return abort_repsonse(500, error=e, message=" Unknown error. Contact service manager.")
        

@user_namespace.route("/")
class UserLogInSuccess(Resource):
    @login_required
    def get(self):
        """GET /user
        ## Get user info
        After logging in on the login page, the token value and email are saved to the browser's local storage.
        Request the API with the value to provide the user's information.
        
        ## Header:
            Authorization (str): login token
            email (str): email
        
        ## Response:
            {"status": "OK", "result": user_info}
        """
        try:
            # TODO: Local storage
            user_email = request.headers.get("email")
            user_info = MySQLManager.get_user_auth(user_email)
            return {"status": "OK", "result": user_info}
        except MySQLManagerError as e:
            return abort_repsonse(500, error=e, message=" Try again in a few minutes.")
        except Exception as e:
            return abort_repsonse(500, error=e, message=" Unknown error. Contact service manager.")



            