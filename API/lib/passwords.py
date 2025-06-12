from common import logger
from bcrypt import gensalt, hashpw, checkpw
from datetime import datetime

def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = gensalt()
    hash_bytes = hashpw(password_bytes, salt)

    return hash_bytes.decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    res = checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    if not res:
        logger.error(f"Password error at {datetime.now()}")

    return res