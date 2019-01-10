import logging
import os

import boto3

dynamodb = boto3.resource('dynamodb')

def get_project_list():
    logging.info("Scanning table for all projects")
    table = dynamodb.Table(os.environ['DYNAMODB_PROJECT_TABLE'])

    result = table.scan()

    if not result['Items']:
        logging.warning(f"Could not find any projects. Table scan result: {result}")
        response = {
            "statusCode": 200,
            "body": "I couldn't find any projects listed. Try adding one!"
        }
    else:        
        response = {
            "statusCode": 200,
            "body": format_response(result['Items'])
        }

    return response
    
def format_response(items):
    string = "*Projects*\n"
    for item in sorted(items, key=lambda item: item['name']):
        name = item['name']
        work_order = item['work_order']
        string += f"- {name}\n"

    return string