# from .common import logger
from .common import get_connection, logger
from .models import ClientCreationInput
from  re import fullmatch
from mariadb import connect, Error as MariaDbError
from .passwords import hash_password

"""
Function to create client
Return a boolean to assert if any errors occurred during the process
"""
def create_client(client_info: ClientCreationInput) -> bool:
    # Assert email is correct
    if not fullmatch(r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+", client_info.email):
        print("eeee")
        return False

    # Verify phone number
    if not fullmatch(r"^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$", client_info.telephone):
        return False

    try:
        connection, cursor = get_connection()

        # Create the client info in client
        cursor.execute("""INSERT INTO Client  (nom, prenom, email, telephone, date_inscription)
        VALUES (?, ?, ?, ?, NOW())""", (client_info.nom, client_info.prenom, client_info.email, client_info.telephone))

        # Retrieve the client_id form client
        client_id = cursor.lastrowid
        if client_id is None:
            logger.error("Can't retrieve the fresh id attributed to the new user !")
            return False

        # hash the password
        password = hash_password(client_info.mot_de_passe)


        # Now adding info to client_password
        cursor.execute("""INSERT INTO Client_Password (client_id, mot_de_passe, date_modification)
        VALUES (?, ?, NOW())""", (client_id, password))

        # At this point every thing went good
        connection.commit()
        return True

    except MariaDbError as e:
        logger.error(f"Failed to add client to db : {e}")
        return False