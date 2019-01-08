import json
import logging
import re
import os

from logs import decimalencoder
from logs.dynamodb_utils import group_db_response_by_date_project
from logs.slack_utils import is_slack_event, slack_post_to_dict, extract_user_id_from_escaped_tag, extract_user_handle_from_escaped_tag

import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')

def list(event, context):
    logging.info("Received event:{}".format(event))
    if not is_slack_event(event):
        logging.warning(f"Rejected list request: {event}")
        return {
            "statusCode": 403,
            "body": "This app is not authorised to do that."
        }
    
    parsed_body = slack_post_to_dict(event)

    command = parsed_body['text']
    user_id = extract_user_id_from_escaped_tag(command)
    if user_id is None:
        logging.error(f"No user ID parsable from command: {command}")
        return {
            "statusCode":400,
            "body":"No valid user provided"
        }
    user_handle = extract_user_handle_from_escaped_tag(parsed_body['command'])
    if user_id is None:
        logging.error(f"No user handle parsable from command: {command}")
        return {
            "statusCode":400,
            "body":"No valid user provided"
        }

    logging.info(f"Scanning table for time logged for {user_id}({user_handle})")
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch all logs for that user from the database
    result = table.scan(
        FilterExpression=Attr('user_id').eq(user_id)
    )

    if not result['Items']:
        logging.warning(f"Could not find time logged for {user_handle}")
        response = {
            "statusCode": 404,
            "body": f"I couldn't find any time logged for @{user_handle}."
        }
    else:
        grouped = group_db_response_by_date_project(result)
        
        response = {
            "statusCode": 200,
            "body": format_response(grouped)
        }

    return response
    
def format_response(grouped_items):
    string = ""
    for date in grouped_items.keys():
        string += f"*{date}*\n"
        projects = grouped_items[date]
        for project in projects:
            string += f"{project}: {projects[project]} minutes\n"
        string += '\n'

    return string