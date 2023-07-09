import uuid
import base64
from unittest import TestCase
from enum import Enum
from lib.db_connect import MySQLManager, RDSManager


MySQLManager = MySQLManager()
RDSManager = RDSManager()


class Mock(Enum):
    """Mock data for testing"""
    EMAIL = "test@test.com"
    NAME = "김테스트"
    PASSWORD = "test123!!"
    DEK=uuid.uuid4().bytes


class MySQLManagerTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        MySQLManager.insert_user_auth(Mock.EMAIL.value, Mock.NAME.value, Mock.PASSWORD.value)
        print("\nSet up module for MySQLManager testing lib/db_connect.py")
    
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
    

class RDSManagerTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        RDSManager.insert_user_dek(Mock.EMAIL.value, Mock.DEK.value)
        print("\nSet up module for testing RDSManager test lib/db_connect.py")
    
    def test_get_user_dek(self):
        result = RDSManager.get_user_dek(Mock.EMAIL.value)
        self.assertEqual(result, Mock.DEK.value)
        
    @classmethod
    def tearDownClass(cls) -> None:
        RDSManager.delete_user_dek(Mock.EMAIL.value)
        print("\nModule Clean.")