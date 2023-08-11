import json
import os
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext


logger = Logger()

class AppConfig:
    """
    Application configuration class. This class is used to set global variables.
    """
    logger.level        = os.environ.get('LOG_LEVEL') or 'INFO'

@logger.inject_lambda_context
def lambda_handler(event: dict, context: LambdaContext):
    """
    _summary_: Parse API Gateway event payload and return a dict
    _param_: event: dict
    _return_: dict
    """

    logger.info(event)
    questions = [
        "How are you?",
        "Whats your name?",
        "How old are you?",
        "Where are you from?",
        "What is your favourite Colour?"
        ]

    json_event = json.loads(event['body'])
    question_event = json_event['question']
    logger.info(json.dumps(question_event))
    logger.info(question_event)
    match question_event:
        case "How are you?":
            response = {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "I am fine, thank you!"
            }
            logger.info(response)
            return response
        case "Whats your name?":
            response = {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "My name is Lambda!"
            }
            logger.info(response)
            return response
        case "How old are you?":
            response = {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "I am 00001 year old!"
            }
            logger.info(response)
            return response
        case "Where are you from?":
            response = {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "I am from the Amazonian Jungles of Seattle, Washington"
            }
            logger.info(response)
            return response
        case "What is your favourite Colour?":
            response = {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "My favourite colour is Yellow"
            }
            logger.info(response)
            return response
        case _:
            response = {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "I'm sorry I don't understand the question.",
                "acceptedOptions": questions
            }
            logger.info(response)
            return response
