import json
import os
import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()

class AppConfig:
    """
    Summary:
    App configuration class. 
    This class is used to store all configuration values for the application.
    The values are read from environment variables.
    """
    sqs_client     = boto3.client('sqs')
    sqs_queue_url  = os.environ.get('SQS_QUEUE_URL')
    role_arn       = os.environ.get('ROLE_ARN')
    region_name    = os.environ.get('REGION_NAME')
    log_level      = os.environ.get('LOG_LEVEL')


class TranslatedEvent:
    """
    Summary:
        A class to translate the event data coming from Signiant's Media Shuttle webhook.
    """
    def __init__(self,
                 time_stamp,
                 event_type,
                 portal_name,
                 portal_url,
                 portal_id,
                 storage_type,
                 storage_id,
                 bucket_name,
                 files
                ):
        """
        Summary:
            Iinitialize the TranslatedEvent class.        
        Args:
            time_stamp (str): _description_
            event_type (str): _description_
            portal_name (str): _description_
            portal_url (str): _description_
            portal_id (str): _description_
            storage_type (str): _description_
            storage_id (str): _description_
            bucket_name (str): _description_
            files (str): _description_
        """
        self.time_stamp     = time_stamp
        self.event_type     = event_type
        self.portal_name    = portal_name
        self.portal_url     = portal_url
        self.portal_id      = portal_id
        self.storage_type   = storage_type
        self.storage_id     = storage_id
        self.bucket_name    = bucket_name
        self.files          = files

def parse_event(webhook_event):
    """
    Summary:
        Parse the event data coming from Signiant's Media Shuttle webhook.
        
    Args:
    webhook_event: dict
        The event data from the webhook.
    """
    event_type      = webhook_event['eventType']

    # If the event is a package upload, parse the data
    if event_type == "package.upload.complete":
        time_stamp      = webhook_event['timestamp']
        payload         = webhook_event['payload']
        portal_details  = payload['portalDetails']
        bucket_name     = portal_details['storage'][0]['configuration']['bucket']
        files = []

        # Loop through the files in the payload and create a list of files
        for file in payload['packageDetails']['files']:

            file_list = {
                    'name': file['path'].replace('Deliveries/', ''),
                    'path': file['path'],
                    'bucket': bucket_name, 
                    'full_path': f"{bucket_name}/{file['path']}",
                    'size_bytes': file['size'],
                    'size_MB': round(file['size'] / 1024 / 1024, 2),
                    }
            files.append(file_list)
        logger.debug(f"Files in package:{files}")
        # Create the TranslatedEvent object
        return_event = TranslatedEvent(
            time_stamp  = time_stamp,
            event_type  = event_type,
            portal_name = portal_details['name'],
            portal_url  = portal_details['url'],
            portal_id   = portal_details['id'],
            storage_type= portal_details['storage'][0]['storageType'],
            storage_id  = portal_details['storage'][0]['id'],
            bucket_name = portal_details['storage'][0]['configuration']['bucket'],
            files       = files
        )
        logger.debug(f"Translated event:{return_event.__dict__}")

        # Return the TranslatedEvent object as a dictionary
        status      = 'success'
        status_code = 200
        response    = {
            'status':status,
            'status_code':status_code,
            'event':return_event.__dict__
            }
        logger.info(response)
        return response
    # If the event is not a package upload, return an error message but not an error code.
    # This will prevent the webhook subscription from being deleted.
    status      = 'error'
    status_code = 204
    response    = {
        'status':status,
        'status_code':status_code,
        'message': 'Event type not supported.'
        }
    logger.error(response)
    return response

def send_message(message):
    """
    Summary:
        Prepare the message to be sent to the SQS queue. 
        Will extract the file names from the event data.

    Args:
        event (dict):
        The event data recieved from the parse_event function.
    """
    file_list = message['event']['files']
    logger.info(f"Number of files in package:{len(file_list)}")
    logger.debug("Files in package:", file_list)
    message_ids = []

    # Loop through the files in the event data and send a message to SQS for each file
    for file in file_list:
        if file is not None:

            logger.debug(f"Sending message to SQS queue for {file['name']}")
            response = AppConfig.sqs_client.send_message(
                QueueUrl=AppConfig.sqs_queue_url,
                MessageBody=json.dumps(file),
                MessageGroupId='SecondaryEvents'
                )
            message_ids.append(response['MessageId'])
    return message_ids

@logger.inject_lambda_context
def lambda_handler(event: dict, context: LambdaContext):
    """event handler lambda function"""

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
