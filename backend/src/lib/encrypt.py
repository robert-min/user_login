import base64
from uuid import uuid4
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class EncryptManager:
    
    def __init__(self) -> None:
        self.Block_size = 16
        
    def get_dek(self) -> bytes:
        try:
            return uuid4().bytes
        except Exception:
            raise EncryptManager("Failed to get dek.")
        
        
    def encrypt_password(self, dek: bytes, origin_pw: str) -> bytes:
        try:
            encoding_pw = origin_pw.encode()
            aes = AES.new(dek, AES.MODE_ECB)    # TODO : MODE_ECB => MODE_CBC 변경 필요!!
            padding_pw = pad(encoding_pw, AES.block_size)
            encrypt_pw = aes.encrypt(padding_pw)
            return base64.b64encode(encrypt_pw)
        except Exception:
            raise EncryptManagerError("Failed to encrypt password.")
    
    def decrypt_password(self, dek: bytes, encrypt_pw: bytes) -> str:
        try:
            aes = AES.new(dek, AES.MODE_ECB)
            decrypt_pw = aes.decrypt(base64.b64decode(encrypt_pw))
            unpadding_pw = unpad(decrypt_pw, AES.block_size)
            return unpadding_pw.decode()
        except Exception:
            raise EncryptManagerError("Failed to decrypt password.")
            
            
class EncryptManagerError(Exception):
    """All EncryptManager Error"""
    