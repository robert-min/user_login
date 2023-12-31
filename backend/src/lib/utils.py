import os
from flask_restx import abort
from pymemcache.client import base
from .db_connect import RDSManager

try:
    CACHE_IP = os.environ["CACHE_IP"] # Dockerimage
except KeyError:
    CACHE_IP = "localhost"

RDSManager = RDSManager()

def get_dek_on_cache(email: str) -> bytes:
    """Get user dek from cache.
    
    Args:
        email: user email
    
    Return:
        dek
    """
    try:
        client = base.Client((CACHE_IP, 11211))
        dek = client.get(email)
    except ConnectionRefusedError:
        dek = RDSManager.get_user_dek(email)
        return dek
    else:
        # If there is no value stored in cache, get DEK from DB.
        if not dek:
            dek = RDSManager.get_user_dek(email)
        # Store DEK in cache.
        client.set(email, dek, expire=600)  # dek expire time 10minute
        return dek

def abort_repsonse(code: int, error: Exception, message: str="") -> None:
    abort(code, status="Fail", message=str(error) + message)
            