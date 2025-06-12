from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    json_response = {"status": "server-up"}
    return json_response