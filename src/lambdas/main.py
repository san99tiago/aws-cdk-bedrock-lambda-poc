# Built-in imports
import logging

# Own imports
from models import QuestionBody
from bedrock_model import BedrockHelper

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
async def execute_model(qbody: QuestionBody):
    """
    FastAPI route that receives a JSON body with a key called "question".
    :param qbody (QuestionBody): The qbody data from the request body.
    :return: Response after executing the AI model.
    """
    # Access the "qbody" key from the received JSON body
    question_text = qbody.question
    logger.info("Executing model with question: %s", question_text)

    bedrock_helper = BedrockHelper()
    result_text = bedrock_helper.execute_model(question_text)

    # Return a dummy response
    return {"message": result_text}


handler = Mangum(app, lifespan="off")
