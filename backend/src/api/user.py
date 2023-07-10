from flask_restx import Namespace, Resource, abort
from flask import request
from . import EncryptManager, MySQLManager, RDSManager, ApiValidator
from lib.encrypt import EncryptManagerError
from lib.db_connect import MySQLManagerError, RDSManagerError
from lib.validator import BadRequestError

user_namespace = Namespace("user")


@user_namespace.route("/create")
class UserCreate(Resource):
    def post(self):
        """
        "email", "name", "password"
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
            return abort_repsonse(500, error=e, message="\nTry again in a few minutes.")
        except MySQLManagerError as e:
            # Delete user DEK stored in RDS in case of MySQL DB error
            RDSManager.delete_user_dek(user_info["email"])
            return abort_repsonse(500, error=e, message="\nTry again in a few minutes.")
        except Exception as e:
            return abort_repsonse(500, error=e, message="\nUnknown error. Contact service manager.")
        
        
def abort_repsonse(code: int, error: Exception, message: str="") -> None:
    abort(code, status="Fail", message=str(error) + message)
            
            