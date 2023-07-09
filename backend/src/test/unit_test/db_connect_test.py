from unittest import TestCase
from enum import Enum
from lib.db_connect import MySQLManager

MySQLManager = MySQLManager()


class Mock(Enum):
    """Mock data for testing"""
    EMAIL = "test@test.com"
    NAME = "김테스트"
    PASSWORD = "test123!!"


class DBconnectionTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        MySQLManager.insert_user_auth(Mock.EMAIL.value, Mock.NAME.value, Mock.PASSWORD.value)
        print("\nSet up module for testing lib/db_connect.py")
    
    def test_get_user_auth(self):
        result = MySQLManager.get_user_auth(Mock.EMAIL.value)
        self.assertEqual(result["email"], Mock.EMAIL.value)
        self.assertEqual(result["name"], Mock.NAME.value)
        self.assertEqual(result["password"], Mock.PASSWORD.value)
    
    def test_get_all_user_auth_email(self):
        result = MySQLManager.get_all_user_auth_email()
        self.assertTrue(result)
        self.assertIn(Mock.EMAIL.value ,result)
    
    @classmethod
    def tearDownClass(cls) -> None:
        MySQLManager.delete_user_auth(Mock.EMAIL.value)
        print("\nModule Clean.")
    
