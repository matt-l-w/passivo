import logging
import os

import boto3
from boto3.dynamodb.conditions import Attr
dynamodb = boto3.resource('dynamodb')

def update_project(name, work_order):
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
        table.put_item(
            Key={'id':project['id']},
            AttributeUpdates={'work_order':work_order})
    except Exception as e:
        logging.error(f"Something went wrong...\n{e}")
        return {
            "statusCode": 200,
            "body": "Sorry, something went wrong.  If this keeps happening, contact an admin"
        }

    response = {
        "statusCode": 200,
        "body": f"Updated the work order for {name} to {wrok_order}"
    }

    return response