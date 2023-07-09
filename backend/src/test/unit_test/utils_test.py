import base64
from unittest import TestCase
from enum import Enum
from uuid import uuid4
from lib.db_connect import RDSManager
from lib.utils import get_dek_on_cache

RDSManager = RDSManager()

class Mock(Enum):
    """Mock data for testing"""
    EMAIL = "test@test.com"
    DEK = b'\xa0\xdbd\x92\x85\xb3I<\xa0\xd9\x9c!m\xc8\xa1C'
    
    
class UtilsTestCase(TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        RDSManager.insert_user_dek(Mock.EMAIL.value, Mock.DEK.value)
        print("\nSet up module for testing lib/utils.py")
        
    def test_get_dek_on_cache(self):
        result = get_dek_on_cache(Mock.EMAIL.value)
        self.assertEqual(result, Mock.DEK.value)

    @classmethod
    def tearDownClass(cls) -> None:
        RDSManager.delete_user_dek(Mock.EMAIL.value)
        print("\nModule Clean.")
    