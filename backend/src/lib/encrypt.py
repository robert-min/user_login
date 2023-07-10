"""Encrypt&Decrypt  library

EncryptManager:
    - 유저 비밀번호 암호화를 위한 Encrypt Manager 입니다.
    Functions:
        - get_dek: 유저별 랜덤으로 대칭키를 생성합니다.
        - encrypt_password: 유저의 비밀번호를 암호화합니다.
        - get_user_auth: 유저의 비밀번호를 복호화합니다.

Raises:
    EncryptManagerError: EncryptManager 클래스에서 발생한 오류

"""
import base64
from uuid import uuid4
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class EncryptManager:
    """
    Encrypt Manager
    """
    
    def __init__(self) -> None:
        self.Block_size = 16
        
    def get_dek(self) -> bytes:
        """Get dek for encryption.
        Return:
            dek
            
        Raise:
            Failed to get dek.
        """
        try:
            return uuid4().bytes
        except Exception:
            raise EncryptManager("Failed to get dek.")
        
        
    def encrypt_password(self, dek: bytes, origin_pw: str) -> bytes:
        """Encrypt password.
        Args:
            dek: user dek
            origin_pw: user password
        
        Return:
            encrypt_pw
            
        Raise:
            Failed to encrypt password.
        """
        try:
            encoding_pw = origin_pw.encode()
            aes = AES.new(dek, AES.MODE_ECB)    # TODO : MODE_ECB => MODE_CBC 변경 필요!!
            padding_pw = pad(encoding_pw, self.Block_size)
            encrypt_pw = aes.encrypt(padding_pw)
            return base64.b64encode(encrypt_pw)
        except Exception:
            raise EncryptManagerError("Failed to encrypt password.")
    
    def decrypt_password(self, dek: bytes, encrypt_pw: bytes) -> str:
        """Decrypt password.
        Args:
            dek: user dek
            encrypt_pw: user encrypt password
        
        Return:
            origin_pw
            
        Raise:
            Failed to decrypt password.
        """
        try:
            aes = AES.new(dek, AES.MODE_ECB)
            decrypt_pw = aes.decrypt(base64.b64decode(encrypt_pw))
            unpadding_pw = unpad(decrypt_pw, self.Block_size)
            return unpadding_pw.decode()
        except Exception:
            raise EncryptManagerError("Failed to decrypt password.")
            
            
class EncryptManagerError(Exception):
    """All EncryptManager Error"""
    