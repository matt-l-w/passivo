import json
import logging
import os

from logs import decimalencoder
from logs.slack_utils import is_slack_event

import boto3
dynamodb = boto3.resource('dynamodb')


def list(event, context):
    logging.info("Received event:{}".format(event))
    if not is_slack_event(event):
        logging.warning(f"Rejected list request: {event}")
        return {
            "statusCode": 403,
            "body": "This app is not authorised to do that."
        }
    
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch all logs from the database
    result = table.scan()

    # create a response
    response = {
        "statusCode": 200,
        "message": json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder)
    }

    return response
