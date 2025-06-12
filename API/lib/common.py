"""
Common py purpose is regrouping all objects reference needed everywhere on the app
such as logger, ...
"""

from logging import basicConfig, INFO, getLogger, DEBUG, ERROR

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