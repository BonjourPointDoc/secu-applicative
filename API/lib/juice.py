from .common import get_connection, logger
from mariadb import Error as MariaDbError
from .models import JuiceItem, JuiceList

def get_all_juice() -> JuiceList:
    try:
        juice_list: list = []

        connection, cursor = get_connection()

        cursor.execute("""SELECT jus_id, nom, prix_unitaire FROM Jus""")

        query = cursor.fetchall()
        if len(query) <= 0:
            logger.error("There's no juices in database or the query as an unknown error !")

        for juice in query:
            if len(juice) != 3:
                logger.warning("One of the juice has the wrong number of values")
                continue # Just pass this juice as we still can try for the others

            try:
                juice_item: JuiceItem = JuiceItem(jus_id= juice[0],
                                                  nom= juice[1],
                                                  prix_unitaire= juice[2])

                juice_list.append(juice_item) # Add this juice to the final list

            except KeyError as e:
                logger.error(f"An key error has occurred when unpacking the values: {e}")
                continue # Pass to the next juice

        # Final return
        return JuiceList(juices= juice_list)
    except MariaDbError as e:
        logger.error(f"Error when fetching juices from database: {e}")
