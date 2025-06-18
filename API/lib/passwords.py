from .common import logger, get_connection
from bcrypt import gensalt, hashpw, checkpw
from datetime import datetime
from time import sleep
from mariadb import Error as MariaDbError

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
    try:
        password_hash: str = ""
        connection, cursor = get_connection()

        cursor.execute("""SELECT Client_Password.mot_de_passe FROM Client 
        INNER JOIN Client_Password
        ON Client.client_id = Client_Password.client_id 
        WHERE Client.email = ?""", (login,))

        query = cursor.fetchone() # Unsafe variable

        if len(query) != 1:
            logger.error("Error when retrieving password hash output not conform")
            return False

        if not isinstance(query[0], str):
            print(type(query[0]))
            logger.error("The password hash from database as wrong format")

        password_hash = query[0]

        return verify_password(password, password_hash)
    except MariaDbError as e:
        logger.error(f"Can't retrieve password: {e}")
        return False

def get_user_hash(client_id: int) -> str:
    connection, cursor = get_connection()

    cursor.execute("""SELECT mot_de_passe 
    FROM Client_Password 
    WHERE client_id = ?""", (client_id,))

    return ""

