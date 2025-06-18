from datetime import datetime, timedelta, timezone
from jwt import encode, decode, DecodeError, ExpiredSignatureError, InvalidTokenError
from os import getenv
from .common import logger

server_secret = getenv("SERVER_SECRET")
if server_secret is None:
    raise ValueError("The server secret environment variable is not set /!\\")



def create_refresh_token(login: str) -> str:
    expiration_time = datetime.now(timezone.utc) + timedelta(days=1)  # Fixing refresh token duration of 1 days
    usr_jwt_token = encode({"login": login, "exp": expiration_time, "refresh": True}, server_secret, algorithm="HS256")
    return usr_jwt_token

def create_access_token(login: str) -> str:
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=15) # Fixing access token duration of 15 minutes
    usr_jwt_token = encode({"login": login, "exp": expiration_time, "refresh": False}, server_secret, algorithm="HS256")
    return usr_jwt_token

def verify_token(token: str, is_refresh: bool) -> bool:
    try:
        json_content = decode(token, server_secret, algorithms="HS256")
        if not json_content:
            logger.error("Failed to decode token !")
            return False

        print(json_content) # Remove in prod
        if not "refresh" in json_content.keys() or not "login" in json_content.keys():
            logger.error("Missing token information aborting")
            return False

        refresh_value = json_content["refresh"]
        if is_refresh: #Whe want to test if it's a refresh token
            if not refresh_value: # Normally it's should be set to True
                logger.error("This is not a refresh token !")
                return False
            return True
        else: # Case where it's an access token
            if refresh_value: # Normally it's should be set to False
                logger.error("This is not an access token !")
                return False
            return True

    except DecodeError:
        logger.error(f"Invalid signature !")
    except ExpiredSignatureError:
        logger.error(f"Token expired !")
    except InvalidTokenError:
        logger.error(f"Invalid token !")

    # Return false to inform that there's a strange request !
    return False

"""
Works for both access and refresh token
This function assumes that the token has already been verified /!\\
"""
def extract_login_from_token(token: str) -> str:
    json_content = decode(token, server_secret, algorithms="HS256")

    return json_content["login"]
