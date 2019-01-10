import logging
import os

import boto3
from boto3.dynamodb.conditions import Attr
dynamodb = boto3.resource('dynamodb')

def remove_project(name):
    table = dynamodb.Table(os.environ['DYNAMODB_PROJECT_TABLE'])

    try:
        result = table.scan(
            FilterExpression=Attr('name').eq(name)
        )
    except Exception as e:
        logging.error(f"Something went wrong...\n{e}")
        return {
            "statusCode": 502,
            "body": "Sorry, something went wrong.  If this keeps happening, contact an admin"
        }

    if not result['Items']:
        logging.warning(f"No projects found for name: {name}")
        return {
            "statusCode": 200,
            "body": "Please enter the name of an existing project."
        }

    project = result['Items'][0]

    try:
        table.delete_item(Key={'id':project['id']})
    except Exception as e:
        logging.error(f"Something went wrong...\n{e}")
        return {
            "statusCode": 200,
            "body": "Sorry, something went wrong.  If this keeps happening, contact an admin"
        }

    response = {
        "statusCode": 200,
        "body": f"Removed {name}"
    }

    return response