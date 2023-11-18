# Built-in imports
import logging

# External imports
from fastapi import FastAPI
from mangum import Mangum

logger = logging.getLogger()


app = FastAPI(
    description="Simple FastAPI server for exposing Bedrock-based PoC experiments",
    contact={"Santiago Garcia Arango": "san99tiago@gmail.com"},
    title="Bedrock PoC Experiments",
    version="0.0.1",
)


@app.get("/")
async def root():
    return {"message": "Hello by Santi"}


@app.get("/status")
async def get_status():
    return {"status": "OK"}


@app.post("/model")
async def execute_model():
    # TODO: Add real berock-based model implementation
    logger.info("Executing model ...")
    logger.debug("processing model ...")
    return {"message": "dummy response"}


handler = Mangum(app, lifespan="off")
