from unittest import TestCase
from enum import Enum
from lib.encrypt import EncryptManager

EncryptManager = EncryptManager()


class Mock(Enum):
    """Mock data for testing"""
    PASSWORD = "test123!!"
    

class EncryptManagerTestCase(TestCase):
        
    @classmethod
    def setUpClass(cls) -> None:
        print("\nSet up module for testing lib/encrypt.py")
    
    def test_get_wdek(self):
        dek = EncryptManager.get_dek()
        self.assertEqual(type(dek), bytes)
    
    def test_encrypt__decrypt_password(self):
        dek = EncryptManager.get_dek()
        encrypt_password = EncryptManager.encrypt_password(dek, Mock.PASSWORD.value)
        self.assertEqual(type(encrypt_password), bytes)
        
        decrypt_password = EncryptManager.decrypt_password(dek, encrypt_password)
        self.assertEqual(decrypt_password, Mock.PASSWORD.value)
        self.assertEqual(type(decrypt_password), str)
