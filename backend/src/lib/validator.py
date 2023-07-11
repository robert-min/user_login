from flask import request
from .db_connect import MySQLManager, RDSManager
from .encrypt import EncryptManager
from .utils import get_dek_on_cache


class ApiValidator:
    def __init__(self):
        self.MySQLManager = MySQLManager()
        self.RDSManager = RDSManager()
        self.EncryptManager = EncryptManager()
        
    
    def check_user_existence(self, email: str) -> None:
        """Check existing email on user_auth"""
        all_user_auth_email = self.MySQLManager.get_all_user_auth_email()
        if email in all_user_auth_email:
            raise BadRequestError("This email already exists. Please log in with your existing account.")
    
    @staticmethod
    def check_user_input(user_info: dict) -> None:
        """Check all valid value for signing user_auth"""
        required_params = ["email", "name", "password"]
        no_input_params = list()
        for param in required_params:
            if param not in user_info.keys() or not user_info[param]:
                no_input_params.append(param)
        
        if no_input_params:
            raise BadRequestError(str(no_input_params) + " was not entered. Please check form.")
    
    def check_login(self, email: str, password: str) -> dict:
        """Check email and password are the same as those stored in the DB."""
        all_user_auth_email = self.MySQLManager.get_all_user_auth_email()
        
        # Check vaild email
        if email not in all_user_auth_email:
            raise UnAuthorizationError("Invalid user email. Please check your email.")
        
        # Check vaild password
        user_auth = self.MySQLManager.get_user_auth(email)
        dek = get_dek_on_cache(email)
        if password != self.EncryptManager.decrypt_password(dek, user_auth["password"]):
            raise UnAuthorizationError("Wrong password. Please check your password.")
    
    @staticmethod
    def check_token_existence(token):
        """Check the token existence"""
        if token is None:
            raise BadRequestError("Token does not exist.")
    
    @staticmethod
    def check_vaild_token_email(decode_token):
        """Check the same headers email and token email"""
        if decode_token["email"] != request.headers.get("email"):
            raise UnAuthorizationError("The wrong approach. Go back to the previous page")
                
            



class BadRequestError(Exception):
    """Bad Request Error : 400"""

class UnAuthorizationError(Exception):
    """UnAuthorization Error : 401"""
    