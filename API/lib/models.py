from pydantic import BaseModel
from enum import Enum

# Model used to define all status
class Status(str, Enum):
    """
    Contains all possibles status
    """
    SUCCESS = "success" # Used to inform that request executed without any errors
    ERROR = "error" # Used to inform that request failed without any further explanation
    WIP = "WIP" # Used temporally in development /!\ SHOULD NOT BE USED IN PROD /!\
    SERVER_UP = "server-up" #Used in / route to inform that API is up an ready to accept requests

# Model used to return Status
class StatusOutput(BaseModel):
    status: Status
    msg: str
    class Config: # Code to raise exceptions when extra fields are added
        extra = "forbid" # New FastAPI way to declare that extra are forbidden

# Model used for logging input
class LoginInput(BaseModel):
    login: str
    password: str
    class Config: # Code to raise exceptions when extra fields are added
        extra = "forbid" # New FastAPI way to declare that extra are forbidden

class LoginOutput(BaseModel):
    status: Status
    api_key: str
    class Config: # Code to raise exceptions when extra fields are added
        extra = "forbid" # New FastAPI way to declare that extra are forbidden
