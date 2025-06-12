from inspect import stack

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from lib.common import logger
from lib.models import Status, StatusOutput ,LoginInput, LoginOutput

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
    # WIP in progress to test framework
    if json_input.login == "fail":  # Used ti simulate wrong credentials
        return JSONResponse(status_code=401,
                            content=StatusOutput(status= Status.ERROR,
                                                 msg= "Wrong crendentials").model_dump())
    output = LoginOutput( # Using LoginOutput model to assert server is sending normal output
        status= Status.WIP,
        api_key= f"bidon key for {json_input.login} + {json_input.password}")

    return output