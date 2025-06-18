from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.params import Header

from lib.models import (Status, StatusOutput ,
                        LoginInput, LoginOutput,
                        ClientCreationInput)
from lib.passwords import *
from lib.token import create_api_key, verify_api_key
from lib.client import create_client

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
        status= Status.WIP,
        api_key= create_api_key(json_input.login))

    return output

@app.get("/token-test", tags=["login"]) # Remove in prod because attacker can brute force token
async def test_token(x_api_key: str = Header(...)):
    if not verify_api_key(x_api_key):
        return JSONResponse(status_code=401,
                            content=StatusOutput(status= Status.ERROR,
                                                 msg="Wrong API Key !").model_dump())

    return StatusOutput(status=Status.SUCCESS, msg="The API key has good format !")

@app.post("/login/user", tags=["login"], response_model=StatusOutput)
async def create_client_route(client_info: ClientCreationInput):
    success = create_client(client_info)

    if not success:
        return JSONResponse(status_code=400,
                            content=StatusOutput(status= Status.ERROR,
                                                 msg="Can't create user !").model_dump())

    return StatusOutput(status= Status.SUCCESS,
                        msg= "User successfully created")