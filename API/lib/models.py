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

# Model used for login input
class LoginInput(BaseModel):
    login: str
    password: str
    class Config: # Code to raise exceptions when extra fields are added
        extra = "forbid" # New FastAPI way to declare that extra are forbidden

# Model used for login output
class LoginOutput(BaseModel):
    status: Status
    api_key: str
    class Config: # Code to raise exceptions when extra fields are added
        extra = "forbid" # New FastAPI way to declare that extra are forbidden

# Model used for creating client account
class ClientCreationInput(BaseModel):
    # Info in table client excluding client_id
    nom: str
    prenom: str
    email: str
    telephone: str
    # Info in client_password excluding mot_de_passe and date_modification
    mot_de_passe: str

# Model used to output the
class AccessTokenOutput(BaseModel):
    status: Status
    access_token: str

# Model used to input the transaction
class TransactionInput(BaseModel):
    address: str

# Model used to return the newest transaction_id created
class TransactionOutput(BaseModel):
    status: Status
    transaction_id: int

# Model used to represent and ingredient
class IngredientDesc(BaseModel):
    ingredient_id: int
    quantite: int
    nom: str

# Model used to represent a recording juice
class JuiceItem(BaseModel):
    jus_id: int
    nom: str
    prix_unitaire: float
    ingredients: list[IngredientDesc]

# Model used to represent the list of juices
class JuiceList(BaseModel):
    juices: list[JuiceItem]

# Model used to add Juice to a transaction.
class JuiceTransactionItem(BaseModel):
    transaction_id: int
    jus_id: int
    quantite: int

# Model used to retrieve the transaction items from database
class TransactionItems(BaseModel):
    juices: list[JuiceTransactionItem]

# Model used to retrieve information from
class TransactionInfo(BaseModel):
    date_transaction: str
    total: float
    adresse_livraison: str

# Model used to change password
class PasswordChange(BaseModel):
    email: str
    old_password: str
    new_password: str

