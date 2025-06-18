"""
Common py purpose is regrouping all objects reference needed everywhere on the app
such as logger, ...
"""

from logging import basicConfig, INFO, getLogger, DEBUG, ERROR
from mariadb import connect, Error as MariaDbError

# Parameters TODO get parameters from a config file
APP_debugging = True

#Initialise logger
basicConfig(
    format="%(levelname)s (APP): %(message)s",
    level=INFO
)
logger = getLogger(__name__)

if APP_debugging:
    logger.setLevel(level=DEBUG)
else:
    logger.setLevel(level=ERROR)  # For production mode logger is set to ERROR

def get_connection():
    conn = None
    try:
        conn = connect(
            user="root",
            password="toto",
            host="127.0.0.1",
            port=3306,
            database="gestion_jus")
    except MariaDbError as e:
        logger.error(f"Error connecting to MariaDB Platform: {e}")

    return conn, conn.cursor()