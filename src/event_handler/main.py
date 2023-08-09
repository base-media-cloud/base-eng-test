import json
import os
import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext


logger = Logger()

class appConfig:
    sqs_queue_url       = os.environ.get('SQS_QUEUE_URL')
    logger.log_level    = os.environ.get('LOG_LEVEL')
    sqs_client          = boto3.client('sqs')

@logger.inject_lambda_context
def lambda_handler(event: dict, context: LambdaContext):
    """
    _summary_: Parse API Gateway event payload and return a dict
    _param_: event: dict
    _return_: dict
    """
    http_method = event.get('httpMethod')
    
    questions = [
        "How are you?",
        "Whats your name?",
        "How old are you?",
        "Where are you from?",
        "What is your favorite colour?",
        "What is your favorite food?"
    ]

    match questions:
        case "How are you?":
            return {
                "statusCode": 200,
                "body": json.dumps("I am fine, thank you!")
            }
        case "Whats your name?":
            return {
                "statusCode": 200,
                "body": json.dumps("My name is Lambda!")
            }
        case "How old are you?":
            return {
                "statusCode": 200,
                "body": json.dumps("I am 00001 year old!")
            }
        case "Where are you from?":
            return {
                "statusCode": 200,
                "body": json.dumps("I am from the Amazonian Jungles of Seattle, Washington")
            }
        case "What is your favourite Colour?":
            return {
                "statusCode": 200,
                "body": "My favourite colour is Yellow"
            }
        case other:
            return {
                "statusCode": 204,
                "body": json.dumps("I'm sorry I don't understand the question.")
                "acceptedOptions": json.dumps(questions)
            }