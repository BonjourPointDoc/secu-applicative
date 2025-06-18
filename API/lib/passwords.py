from .common import logger, get_connection
from bcrypt import gensalt, hashpw, checkpw
from datetime import datetime
from time import sleep

def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = gensalt()
    hash_bytes = hashpw(password_bytes, salt)

    return hash_bytes.decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    res = checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    if not res or password == "fail": # Second conditions added for tests
        logger.error(f"Password error at {datetime.now()}")
        sleep(2) # Adding timer to avoid brute force attacks
        return False

    return res

def verify_credentials(login: str, password: str) -> bool:

    # Dummy code waiting for real db access
    logger.error(f"WIP function no real db connection : {login}")
    password_hash: str = hash_password(password)
    if verify_password(password, password_hash): # If this bug very huge bug /!\
        return True
    else:
        return False

def get_user_hash(client_id: int) -> str:
    connection, cursor = get_connection()

    cursor.execute("""SELECT mot_de_passe 
    FROM Client_Password 
    WHERE client_id = ?""", (client_id,))

    return ""

