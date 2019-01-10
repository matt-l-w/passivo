import logging
import os
import time
import uuid

import boto3
dynamodb = boto3.resource('dynamodb')

def add_project(name, work_order):
    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['DYNAMODB_PROJECT_TABLE'])

    item = {
        'id': str(uuid.uuid1()),
        'name': name,
        'work_order': work_order,
        'createdAt': timestamp,
    }

    try:
        table.put_item(Item=item)
    except Exception as e:
        logging.error(f"Something went wrong...\n{e}")
        return {
            "statusCode": 200,
            "body": "Sorry, something went wrong.  If this keeps happening, contact an admin"
        }

    response = {
        "statusCode": 200,
        "body": f"Added {name} with work order {work_order}"
    }

    return response