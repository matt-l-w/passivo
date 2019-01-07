from urllib.parse import parse_qs

def slack_post_to_dict(event):
    event_body = event['body']
    parsed = parse_qs(event_body)
    trimmed = {k.strip(): v[0].strip() for k, v in parsed.items()}
    return trimmed