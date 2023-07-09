from unittest import TestCase
from enum import Enum
from lib.db_connect import DBManager

DBManager = DBManager()


class Mock(Enum):
    """Mock data for testing"""
    EMAIL = "test@test.com"
    NAME = "김테스트"
    PASSWORD = "test123!!"


class DBconnectionTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        DBManager.insert_user_auth(Mock.EMAIL, Mock.NAME, Mock.PASSWORD)
        print("\nSet up module for testing lib/db_connect.py")
        
    @classmethod
    def tearDownClass(cls) -> None:
        DBManager.delete_user_auth(Mock.EMAIL)
        print("\nModule Clean.")
    
