from .common import get_connection, logger
from mariadb import Error as MariaDbError
from .models import JuiceItem, JuiceList, IngredientDesc

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
                ingredients_desc: list[IngredientDesc] = get_juice_composition_info(juice[0])

                juice_item: JuiceItem = JuiceItem(jus_id= juice[0],
                                                  nom= juice[1],
                                                  prix_unitaire= juice[2],
                                                  ingredients= ingredients_desc)

                juice_list.append(juice_item) # Add this juice to the final list

            except KeyError as e:
                logger.error(f"An key error has occurred when unpacking the values: {e}")
                continue # Pass to the next juice

        # Final return
        return JuiceList(juices= juice_list)
    except MariaDbError as e:
        logger.error(f"Error when fetching juices from database: {e}")


def get_juice_price(jus_id: int) -> float:
    try:
        connection, cursor = get_connection()

        cursor.execute("""SELECT prix_unitaire FROM Jus
        WHERE jus_id = ?""", (jus_id,))

        query = cursor.fetchone()

        if len(query) != 1:
            logger.error("Database return wrong number of information")
            return -1

        if not isinstance(float(query[0]), float):
            logger.error("Database return wrong type for the price !")
            return -1

        # Good case
        return float(query[0])



    except MariaDbError as e:
        logger.error(f"Failed to gather juice price from database: {e}")
    except KeyError:
        logger.error("This error should never occur as long as checks above should avoid it !")


    return -1 # To inform that there's an error

def get_juice_composition_info(juice_id: int) -> list[IngredientDesc]:
    try:
        connection, cursor = get_connection()

        cursor.execute("""SELECT Jus_Ingredient.ingredient_id, Jus_Ingredient.quantite, Ingredient.nom
        FROM Jus_Ingredient INNER JOIN Ingredient ON Jus_Ingredient.ingredient_id = Ingredient.ingredient_id
        WHERE Jus_Ingredient.jus_id = ?""", (juice_id,))

        query = cursor.fetchall()

        if len(query) < 1:
            logger.error("Juice has no ingredients !")
            return []

        ingredient_list: list[IngredientDesc] = []
        for ingredient in query:
            if len(ingredient) != 3:
                logger.error("Not the correct number of ingredient info from database")
                continue

            obj: IngredientDesc = IngredientDesc(ingredient_id= ingredient[0],
                                                 quantite= float(ingredient[1]),
                                                 nom= ingredient[2])

            ingredient_list.append(obj)

        return ingredient_list


    except MariaDbError as e:
        logger.error(f"Can't retrieve ingredient informations: {e}")