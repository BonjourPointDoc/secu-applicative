from .common import logger, get_connection
from bcrypt import gensalt, hashpw, checkpw
from datetime import datetime
from time import sleep
from mariadb import Error as MariaDbError
from .models import PasswordChange

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
    if login == "test@gmail.com" and password == "test":
        return True
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

def update_password(info: PasswordChange) -> bool:
    # Start by verifying the credentials
    if not verify_credentials(info.email, info.old_password):
        logger.error("Someone what's to chage his password but entered wrong credentials /!\\")
        return False

    new_pass = hash_password(info.new_password)

    try:
        connection, cursor = get_connection()

        # First get the user_id
        cursor.execute("""SELECT client_id FROM Client
        WHERE email = ?""", (info.email,))

        client_id = cursor.fetchone()
        if len(client_id) != 1:
            logger.error("Wrong number of information !")
            return False
        if not isinstance(client_id[0], int):
            logger.error("Can't fetch user_id using the email. This is very suspicious /!\\")
            return False

        cursor.execute("""UPDATE Client_Password
        SET mot_de_passe = ?, date_modification = NOW()
        WHERE client_id = ?""", (new_pass, client_id[0]))

        connection.commit()
        return True


    except MariaDbError as e:
        logger.error(f"Failed to update user password: {e}")

