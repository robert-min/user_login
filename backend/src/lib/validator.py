from .db_connect import MySQLManager


class ApiValidator:
    def __init__(self):
        self.MySQLManager = MySQLManager()
        
    
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
            if param not in user_info.keys():
                no_input_params.append(param)
        
        if no_input_params:
            raise BadRequestError(str(no_input_params) + " was not entered. Please check form.")
        
class BadRequestError(Exception):
    """Bad Request Error : 400"""
