from .common import get_connection, logger
from mariadb import Error as MariaDbError
from .client import get_client_id_by_token

"""
For creating the transaction whe only the client we just need the client id 
as whe don't know other information
"""
def create_transaction(token: str) -> bool:
    client_id = get_client_id_by_token(token)
    if not client_id > 0:
        logger.error("Error when getting the client_id for creating the transaction")
        return False

    try:
        connection, cursor = get_connection()

        cursor.execute("""INSERT INTO Transaction
        (client_id, date_transaction, total) 
        VALUES (?,NOW(),0)""", (client_id,))

        connection.commit()

    except MariaDbError as e:
        logger.error(f"Can't create a transaction : {e}")
        return False


    return True
