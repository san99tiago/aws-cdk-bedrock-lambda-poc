# Built-in imports
import logging

# External imports
from fastapi import FastAPI, Body
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


@app.post("/model")
async def execute_model(question: dict = Body(...)):
    """
    FastAPI route that receives a JSON body with a key called "question".
    :param question: The question data from the request body.
    :return: Response with a dummy message.
    """
    # Access the "question" key from the received JSON body
    question_text = question.get("question", "")

    # TODO: Use the question_text in your Bedrock-based model implementation

    # Log information about the execution
    logger.info("Executing model with question: %s", question_text)
    logger.debug("Processing model ...")

    # Return a dummy response
    return {"message": "dummy response"}


handler = Mangum(app, lifespan="off")
