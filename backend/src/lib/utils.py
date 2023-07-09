from pymemcache.client import base
from .db_connect import RDSManager

CACHE_IP = "localhost"
RDSManager = RDSManager()

def get_dek_on_cache(email: str):
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
        return RDSManager.get_user_dek(email)
    else:
        # If there is no value stored in cache, get DEK from DB.
        if not dek:
            dek = RDSManager.get_user_dek(email)
        # Store DEK in cache.
        client.set(email, dek, expire=600)  # dek expire time 10minute
        return dek
