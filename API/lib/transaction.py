from operator import index

from .common import get_connection, logger
from mariadb import Error as MariaDbError
from .client import get_client_id_by_token
from .models import TransactionInput, JuiceTransactionItem, TransactionItems

"""
For creating the transaction whe only the client we just need the client id 
as whe don't know other information
Value -1 means there's an error
"""
def create_transaction(token: str, info: TransactionInput) -> int: # Passed to int to inform give the command id
    client_id = get_client_id_by_token(token)
    if not client_id > 0:
        logger.error("Error when getting the client_id for creating the transaction")
        return -1

    try:
        connection, cursor = get_connection()

        cursor.execute("""INSERT INTO Transaction
        (client_id, date_transaction, total, adresse_livraison) 
        VALUES (?,NOW(),0, ?)""", (client_id, info.address))

        res = cursor.lastrowid
        connection.commit()

    except MariaDbError as e:
        logger.error(f"Can't create a transaction : {e}")
        return -1


    return res

def add_juice_to_transaction(juice_info: JuiceTransactionItem, token: str) -> bool:
    try:
        connection, cursor= get_connection()
        user_id = get_client_id_by_token(token)

        cursor.execute("""SELECT COUNT(transaction_id) FROM Transaction
        WHERE client_id = ? AND transaction_id = ?""", (user_id, juice_info.transaction_id))


        try:
            if cursor.fetchone()[0] != 1:
                logger.error("User don't own this transaction")
                return False
        except IndexError:
            logger.error("User don't own this transaction")
            return False

        cursor.execute("""INSERT INTO Transaction_Jus
        (transaction_id, jus_id, quantite)
        VALUES (?, ?, ?)""", (juice_info.transaction_id, juice_info.jus_id, juice_info.quantite))

        connection.commit()
        return True
    except MariaDbError as e:
        logger.error(f"Failed to add juice to the transaction: {e}")
        return False

def get_transaction_items(token: str, transaction_id: int) -> TransactionItems:
    try:
        connection, cursor= get_connection()
        user_id = get_client_id_by_token(token)

        cursor.execute("""SELECT COUNT(transaction_id) FROM Transaction
        WHERE client_id = ? AND transaction_id = ?""", (user_id, transaction_id))


        try:
            if cursor.fetchone()[0] != 1:
                logger.error("User don't own this transaction")
                return TransactionItems(juices= [])
        except IndexError:
            logger.error("User don't own this transaction")
            return TransactionItems(juices= [])


        juices_item: list = []

        cursor.execute("""SELECT transaction_id, jus_id, quantite FROM Transaction_Jus
        WHERE transaction_id = ?""", (transaction_id,))

        query = cursor.fetchall()

        if len(query) < 1:
            # No need to log an error because it means that no item have been added.
            return TransactionItems(juices= [])

        for item in query:
            if len(item) != 3:
                logger.error("An transaction_jus item has an invalid number of values ")
                continue # Just pass to the next item

            try:
                obj: JuiceTransactionItem = JuiceTransactionItem(transaction_id= item[0],
                                                                 jus_id= item[1],
                                                                 quantite= item[2])
                juices_item.append(obj)

            except IndexError:
                logger.error("This error should never happened /!\\ This means that's further verification are not working correctly !")
                continue

        return TransactionItems(juices= juices_item)
    except MariaDbError as e:
        logger.error(f"Failed to add juice to the transaction: {e}")
        return TransactionItems(juices= [])



def update_juice_to_transaction(juice_info: JuiceTransactionItem, token: str) -> bool:
    try:
        connection, cursor= get_connection()
        user_id = get_client_id_by_token(token)

        cursor.execute("""SELECT COUNT(transaction_id) FROM Transaction
        WHERE client_id = ? AND transaction_id = ?""", (user_id, juice_info.transaction_id))


        try:
            if cursor.fetchone()[0] != 1:
                logger.error("User don't own this transaction")
                return False
        except IndexError:
            logger.error("User don't own this transaction")
            return False

        # Get the actual values
        cursor.execute("""SELECT transaction_id, jus_id, quantite FROM Transaction_Jus
        WHERE transaction_id = ? AND jus_id = ?""", (juice_info.transaction_id, juice_info.jus_id))

        query = cursor.fetchone()

        if not query:
            logger.warning("This is a new item to add to transaction. Please use post method !")
            return False

        if len(query) != 3:
            logger.error("Wrong number of values fetched from database !")


        if juice_info.quantite != query[2]: # Assert if the value has changed
            cursor.execute("""UPDATE Transaction_Jus
            SET quantite = ?
            WHERE transaction_id = ? AND jus_id = ?""", (juice_info.quantite, juice_info.transaction_id, juice_info.jus_id))

            connection.commit()
            return True

        else:
            return True # Even if nothing has changed there's no errors

    except MariaDbError as e:
        logger.error(f"Failed to add juice to the transaction: {e}")
        return False