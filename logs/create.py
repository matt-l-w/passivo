import json
import logging
import os
import time
import uuid
import re

from utils.slack_utils import slack_post_to_dict, is_slack_event
from projects.list import get_project_list

import boto3
dynamodb = boto3.resource('dynamodb')


def create(event, context):
    logging.info("Received event:{}".format(event))
    if not is_slack_event(event):
        return {
            "statusCode": 403,
            "message": "This app is not authorised to do that."
        }

    parsed_body = slack_post_to_dict(event)
    text = parsed_body['text']
    user_id = parsed_body['user_id']
    
    minutes = parse_minutes(text)
    project = parse_project(text)
    if not minutes or not project:
        logging.error("Couldn't parse '{}'".format(text))
        logging.error("Original request '{}'".format(parsed_body))
        return {"statusCode": 200, "body": "Sorry, I couldn't understand you. Try 'X minutes _on_ project'"}

    project_list = get_project_list()
    project_names = list(map(lambda p: p['name'], project_list))
    if project not in project_names:
        formatted_project_list = "\n".join(project_names)
        return {
            "statusCode": 200,
            "body": f"I couldn't find {project} in the list of available projects.  Here's all the ones I know:\n{formatted_project_list}"
        }
    
    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['DYNAMODB_LOG_TABLE'])

    item = {
        'id': str(uuid.uuid1()),
        'user_id': user_id,
        'command': text,
        'minutes': minutes,
        'project': project,
        'createdAt': timestamp,
    }

    # write the log entry to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "body": "Logged {} minutes on {}".format(minutes, project)
    }

    return response

def parse_minutes(command):
    """
    Match 1: any number of digits at the beginning of the command.
    Match 2: any text following the digits before the next whitespace.
    """
    search = re.search('^([0-9]+)\s?([a-zA-Z]+)', command)
    if search:
        value = search.group(1)
        unit = search.group(2)[0]
    else:
        return None

    if unit in [
        'h',
        'hs',
        'hr',
        'hrs',
        'hour',
        'hours']:
        value = str(int(value)*60)

    return value

def parse_project(command):
    """
    Match 1: any text after 'on'.  Quotes escaped.
    """
    search = re.search('(?<=\ on\ )\'?\"?([\w\ ]*)\'?\"?$', command)
    if search:
        return search.group(1)
    
    return None