import hmac
import hashlib
import logging
import re
import time
from os import getenv
from urllib.parse import parse_qs

def slack_post_to_dict(event):
    event_body = event['body']
    parsed = parse_qs(event_body)
    trimmed = {k.strip(): v[0].strip() for k, v in parsed.items()}
    return trimmed

def is_slack_event(event, current_time=None):
    if current_time is None: current_time = time.time()
    slack_signing_secret = getenv('SLACK_SIGNING_SECRET')
    if not slack_signing_secret:
        raise AttributeError("SLACK_SIGNING_SECRET env var not set.")

    headers = event['headers']
    timestamp = read_header_or_return('X-Slack-Request-Timestamp',headers)
    if not timestamp: return False

    if abs(current_time - float(timestamp)) > 60 * 5:
        # The request timestamp is more than five minutes from local time.
        # It could be a replay attack, so let's ignore it.
        logging.warning(f"Current time {current_time} was greater than 5 mins away.  Rejected in case of replay attack.")
        return False

    body = event['body']

    sig_basestring = f"v0:{timestamp}:{body}".encode('utf-8')

    my_signature = 'v0=' + hmac.new(
        bytes(slack_signing_secret, 'utf-8'),
        sig_basestring,
        hashlib.sha256
    ).hexdigest()

    slack_signature = read_header_or_return('X-Slack-Signature', headers)
    if not slack_signature: return False

    if hmac.compare_digest(my_signature, slack_signature):
        return True
    
    logging.warning(f"Verification failed.\nmy_signature: {my_signature}\nslack_signature: {slack_signature}")
    return False

def read_header_or_return(header, headers):
    try:
        return headers[header]
    except KeyError:
        logging.error(f"Unable to read '{header}' header from event with headers: {headers}")
        return None

def extract_user_id_from_escaped_tag(command):
    """
    Extract a user ID from an escaped handle provided by slack
    """
    search = re.search('\<\@(\w+)', command)
    if search:
        return search.group(1)
    else:
        return None

def extract_user_handle_from_escaped_tag(command):
    """
    Extract a user handle from an escaped handle provided by slack
    """
    search = re.search('\|([\w.]+)\>', command)
    if search:
        return search.group(1)
    else:
        return None