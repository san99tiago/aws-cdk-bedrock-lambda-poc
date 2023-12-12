# Built-in imports
import logging
import json
import boto3


logger = logging.getLogger()
bedrock = boto3.client("bedrock-runtime")


class BedrockHelper:
    def __init__(self, max_tokens: int = 1525, temperature: float = 0.7):
        self.max_tokens = max_tokens
        self.temperature = temperature
        # TODO: update the class to allow additional models
        self.model_id = "ai21.j2-ultra-v1"

    def execute_model(self, prompt: str) -> str:
        logger.info(f"Starting Bedrock execute_model method with prompt: {prompt}")
        # Note: if needed, we could enhance the prompt to guarantee better agent/system design

        body = json.dumps(
            {
                "prompt": prompt,
                "maxTokens": self.max_tokens,
                "temperature": self.temperature,
                "topP": 1,
                "stopSequences": [],
                "countPenalty": {"scale": 0},
                "presencePenalty": {"scale": 0},
                "frequencyPenalty": {"scale": 0},
            }
        )

        response = bedrock.invoke_model(
            body=body,
            modelId=self.model_id,
            accept="application/json",
            contentType="application/json",
        )

        logger.debug(f"bedrock.invoke_model response is: {response}")

        response_body = json.loads(response.get("body").read())
        result_text = (
            response_body.get("completions")[0].get("data").get("text").strip()
        )

        logger.info(f"response completitions [0] text is: {result_text}")

        return result_text
