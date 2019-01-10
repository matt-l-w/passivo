import logging

from utils.slack_utils import is_slack_event, slack_post_to_dict

from projects.list import get_project_list
from projects.add import add_project
from projects.remove import remove_project
from projects.update import update_project

help_text = "*Passivo Help*\nWith the `project` command you can manage the projects and their associated work orders.\n\
`list` will list the available projects\n\
`add project_name work_order` will add a new project/work order combination\n\
`update project_name work_order` will update an existing project/work order combination\n\
`remove project_name` will remove an existing project."

def handler(event, context):
    logging.info("Received event:{}".format(event))
    if not is_slack_event(event):
        logging.warning(f"Rejected list request: {event}")
        return {
            "statusCode": 403,
            "body": "This app is not authorised to do that."
        }
    
    parsed_body = slack_post_to_dict(event)

    command_words = parsed_body['text'].split(' ')
    command = command_words[0]

    if command == "help":
        return {
            "statusCode": 200,
            "body": help_text
        }
    if command == "list":
        return get_project_list()

    elif command == "add":
        name = ' '.join(command_words[1:-1]).replace("\"","").replace("\'", "")
        work_order = command_words[-1]
        return add_project(name, work_order)

    elif command == "update":
        name = ' '.join(command_words[1:-1]).replace("\"","").replace("\'", "")
        work_order = command_words[-1]
        return update_project(name, work_order)

    elif command == "remove":
        name = ' '.join(command_words[1:])
        return remove_project(name)

    else:
        logging.error(f"Couldn't parse command from {command}")
        return {
            "statusCode": 200,
            "body": "Sorry, I couldn't understand that command. Try `/project help`"
        }
    
