from datetime import datetime, timedelta, timezone
from jwt import encode, decode, DecodeError, ExpiredSignatureError, InvalidTokenError
from os import getenv
from .common import logger

server_secret = getenv("SERVER_SECRET")
if server_secret is None:
    raise ValueError("The server secret environment variable is not set /!\\")



def create_api_key(login: str) -> str:
    expiration_time = datetime.now(timezone.utc) + timedelta(weeks=10)  # Fixing token validity duration by 10 week
    usr_jwt_token = encode({"login": login, "exp": expiration_time}, server_secret, algorithm="HS256")
    return usr_jwt_token

def verify_api_key(token: str) -> bool:
    try:
        json_content = decode(token, server_secret, algorithms="HS256")
        if not json_content:
          logger.error("Failed to decode token !")
        return True

    except DecodeError:
        logger.error(f"Invalid signature !")
    except ExpiredSignatureError:
        logger.error(f"Token expired !")
    except InvalidTokenError:
        logger.error(f"Invalid token !")

    # Return false to inform that there's a strange request !
    return False