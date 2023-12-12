from pydantic import BaseModel


class QuestionBody(BaseModel):
    question: str
