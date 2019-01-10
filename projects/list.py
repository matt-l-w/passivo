import logging
import os

import boto3

dynamodb = boto3.resource('dynamodb')

def get_project_list():
    logging.info("Scanning table for all projects")
    table = dynamodb.Table(os.environ['DYNAMODB_PROJECT_TABLE'])

    result = table.scan()

    return result['Items']
    
def format_response(items):
    logging.info(f"Formatting: {items}")
    if not items:
        logging.warning("Could not find any projects.")
        return {
            "statusCode": 200,
            "body": "I couldn't find any projects listed. Try adding one!"
        }

    string = "*Projects*\n"
    for item in sorted(items, key=lambda x: x['name']):
        name = item['name']
        work_order = item['work_order']
        string += f"- {name} : {work_order}\n"

    return {
        "statusCode": 200,
        "body": string
    }