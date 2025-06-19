from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.params import Header

from lib.common import logger
from lib.passwords import verify_credentials, update_password
from lib.token import create_refresh_token, create_access_token, verify_token, extract_login_from_token
from lib.client import create_client
from lib.transaction import create_transaction, add_juice_to_transaction, get_transaction_items, update_juice_to_transaction, update_total, get_transaction_info
from lib.juice import get_all_juice
from lib.models import (Status, StatusOutput ,
                        LoginInput, LoginOutput,
                        ClientCreationInput, PasswordChange,
                        AccessTokenOutput,
                        TransactionInput, TransactionOutput, JuiceTransactionItem, TransactionItems, TransactionInfo,
                        JuiceList)


# Initialise API
app = FastAPI(title="Juice shop", version="beta")

@app.get("/", tags=["Temporary dev"])
async def root():
    logger.debug("Logging is working !")
    json_response = {"status": "server-up"}
    return json_response

@app.post("/login", tags=["login"], response_model=LoginOutput,
          responses={401: {"model": LoginOutput, "description": "Wrong credentials"}})
async def login(json_input: LoginInput):
    if not verify_credentials(json_input.login, json_input.password):
        return JSONResponse(status_code=401,
                            content=StatusOutput(status= Status.ERROR,
                                                 msg= "Wrong credentials").model_dump())
    output = LoginOutput( # Using LoginOutput model to assert server is sending normal output
        status= Status.SUCCESS,
        api_key= create_refresh_token(json_input.login))

    return output

@app.patch("/login", tags=["login"])
async def change_password_route(password_infos: PasswordChange):
    if not update_password(password_infos):
        return JSONResponse(status_code=400, content= StatusOutput(status= Status.ERROR,
                                                                   msg= "Can't update password").model_dump())
    return StatusOutput(status= Status.SUCCESS, msg= "Password updated successfully")

"""
# Remove in prod because attacker can brute force token
@app.post("/token/access/test", tags=["login"], response_model=StatusOutput,
         responses={200: {"model": StatusOutput},
                    401: {"model": StatusOutput}})
async def test_token(x_api_key: str = Header(...)):
    if not verify_token(x_api_key, False): # False is for access token
        return JSONResponse(status_code=401,
                            content=StatusOutput(status= Status.ERROR,
                                                 msg="Wrong API Key !").model_dump())

    return StatusOutput(status=Status.SUCCESS, msg="The API key has good format !")
"""

@app.post("/login/user", tags=["login"], response_model=StatusOutput,
          responses={200: {"model": StatusOutput},
                     400: {"model": StatusOutput}})
async def create_client_route(client_info: ClientCreationInput):
    success = create_client(client_info)

    if not success:
        return JSONResponse(status_code=400,
                            content=StatusOutput(status= Status.ERROR,
                                                 msg="Can't create user !").model_dump())

    return StatusOutput(status= Status.SUCCESS,
                        msg= "User successfully created")

@app.post("/token/access", tags=["login"], response_model=AccessTokenOutput,
          responses= {200: {"model": AccessTokenOutput},
                      401: {"model": StatusOutput}})
async def get_access_token_route(x_api_key: str = Header(...)):
    if not verify_token(x_api_key, True): # We want a refresh token here
        return JSONResponse(status_code=401 ,content=StatusOutput(status= Status.ERROR,
                            msg= "Token rejected").model_dump())

    access_token: str = create_access_token(extract_login_from_token(x_api_key))

    return AccessTokenOutput(status= Status.SUCCESS,
                             access_token= access_token).model_dump()

@app.post("/transaction", tags=["transaction"])
async def add_transaction_route(transaction_info: TransactionInput,x_api_key: str = Header(...)):
    if not verify_token(x_api_key, False): # Access token
        return JSONResponse(status_code=401 ,content=StatusOutput(status= Status.ERROR,
                            msg= "Token rejected").model_dump())

    transaction_id = create_transaction(x_api_key, transaction_info)
    if transaction_id == -1 : # -1 means that an error occurred
        return JSONResponse(status_code=400, content=StatusOutput(status= Status.ERROR,
                                                                  msg= "Failed to create transaction"))

    return TransactionOutput(status= Status.SUCCESS,
                             transaction_id= transaction_id).model_dump()

@app.get("/juice", tags=["juice"], response_model=JuiceList)
async def get_all_juice_route(x_api_key: str = Header(...)):
    if not verify_token(x_api_key, False): # Access token
        return JSONResponse(status_code=401 ,content=StatusOutput(status= Status.ERROR,
                            msg= "Token rejected").model_dump())

    all_juice: JuiceList = get_all_juice()

    return all_juice.model_dump()

@app.post("/transaction/add-juice", tags=["transaction"])
async def add_juice_to_transaction_route(juice_info: JuiceTransactionItem, x_api_key: str = Header(...)):
    if not verify_token(x_api_key, False): # Access token
        return JSONResponse(status_code=401 ,content=StatusOutput(status= Status.ERROR,
                            msg= "Token rejected").model_dump())

    if not add_juice_to_transaction(juice_info, x_api_key):
        return JSONResponse(status_code=400, content=StatusOutput(status= Status.ERROR,
                                                                  msg="Failed to add juice to transaction").model_dump())
    # Automatically update total of transaction
    update_total(juice_info.transaction_id, x_api_key)

    return StatusOutput(status= Status.SUCCESS, msg= "Successfully added juice to transaction").model_dump()


@app.patch("/transaction", tags=["transaction"], response_model=StatusOutput)
async def update_juice_from_transaction_route(juice_info: JuiceTransactionItem, x_api_key: str = Header(...)):
    if not verify_token(x_api_key, False):  # Access token
        return JSONResponse(status_code=401, content=StatusOutput(status=Status.ERROR,
                                                                  msg="Token rejected").model_dump())

    if not update_juice_to_transaction(juice_info, x_api_key):
        return JSONResponse(status_code=400, content=StatusOutput(status= Status.ERROR,
                                                                  msg="Can't update transaction").model_dump())

    # Automatically update total of transaction
    update_total(juice_info.transaction_id, x_api_key)

    return StatusOutput(status= Status.SUCCESS,
                        msg= "Successfully updated juice on the transaction").model_dump()

@app.get("/transaction_info", tags=["transaction"], response_model=TransactionInfo)
async def get_transaction_info_route(transaction_id: int, x_api_key: str = Header(...)):
    if not verify_token(x_api_key, False):  # Access token
        return JSONResponse(status_code=401, content=StatusOutput(status=Status.ERROR,
                                                                  msg="Token rejected").model_dump())

    res = get_transaction_info(x_api_key, transaction_id)
    if res.total < 0:
        return  JSONResponse(status_code=400, content=StatusOutput(status= Status.ERROR,
                                                                   msg= "Can't retrieve transaction info"))

    return res.model_dump()

@app.get("/transaction/juice", tags=["transaction"], response_model=TransactionItems)
async def get_transaction_route(transaction_id: int, x_api_key: str = Header(...)):
    if not verify_token(x_api_key, False):  # Access token
        return JSONResponse(status_code=401, content=StatusOutput(status=Status.ERROR,
                                                                  msg="Token rejected").model_dump())

    items: TransactionItems = get_transaction_items(x_api_key, transaction_id)

    return items.model_dump()

