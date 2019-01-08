import hmac
import hashlib
import time

from unittest import TestCase, mock

class TestSlackParse(TestCase):
    slack_example = "\
        token=gIkuvaNzQIHg97ATvDxqgjtO\
        &team_id=T0001\
        &team_domain=example\
        &enterprise_id=E0001\
        &enterprise_name=Globular%20Construct%20Inc\
        &channel_id=C2147483705\
        &channel_name=test\
        &user_id=U2147483697\
        &user_name=Steve\
        &command=/weather\
        &text=94070\
        &response_url=https://hooks.slack.com/commands/1234/5678\
        &trigger_id=13345224609.738474920.8088930838d88f008e0"

    def test_www_form_urlencoded_parsed(self):
        from logs.slack_utils import slack_post_to_dict
        event = {
            'body': self.slack_example
        }

        expected = dict()
        expected['token'] = 'gIkuvaNzQIHg97ATvDxqgjtO'
        expected['team_id'] = 'T0001'
        expected['team_domain'] = 'example'
        expected['enterprise_id'] = 'E0001'
        expected['enterprise_name'] = 'Globular Construct Inc'
        expected['channel_id'] = 'C2147483705'
        expected['channel_name'] = 'test'
        expected['user_id'] = 'U2147483697'
        expected['user_name'] = 'Steve'
        expected['command'] = '/weather'
        expected['text'] = '94070'
        expected['response_url'] = 'https://hooks.slack.com/commands/1234/5678'
        expected['trigger_id'] = '13345224609.738474920.8088930838d88f008e0'

        self.assertEqual(
            slack_post_to_dict(event),
            expected)
        
class TestSlackValidation(TestCase):

    def test_no_secret_raises_exception(self):
        from logs.slack_utils import is_slack_event

        with self.assertRaises(AttributeError):
            is_slack_event({})

    @mock.patch.dict('os.environ', {'SLACK_SIGNING_SECRET': 'mysecret'})
    def test_returns_true_when_signatures_match(self):
        from logs.slack_utils import is_slack_event
        
        current_time = time.time()
        slack_signing_secret = bytes('mysecret', 'utf-8')
        sig_basestring = f"v0:{current_time}:bodytext".encode('utf-8')

        test_slack_signature = 'v0=' + hmac.new(slack_signing_secret, sig_basestring, hashlib.sha256).hexdigest()

        test_event = {
            'headers':{
                'X-Slack-Signature': test_slack_signature,
                'X-Slack-Request-Timestamp': current_time
            },
            'body':'bodytext'
        }

        self.assertTrue(is_slack_event(test_event, current_time))


class TestReadHeader(TestCase):

    def test_header_present_returns_header(self):
        from logs.slack_utils import read_header_or_return

        self.assertEqual(
            read_header_or_return('header1', {'header1': 'value'}),
            'value')

    def test_header_not_present_returns_none(self):
        from logs.slack_utils import read_header_or_return

        self.assertIsNone(read_header_or_return('header1', {}))


class TestExtractUserId(TestCase):

    def test_no_user_id_returns_none(self):
        from logs.slack_utils import extract_user_id_from_escaped_tag
        self.assertIsNone(extract_user_id_from_escaped_tag('something else'))

    def test_user_id_extracted_from_command(self):
        from logs.slack_utils import extract_user_id_from_escaped_tag
        id = extract_user_id_from_escaped_tag('<@U1234|andyP>')

        self.assertEqual(id, 'U1234')

class TestExtractUserHandle(TestCase):

    def test_no_user_handle_returns_none(self):
        from logs.slack_utils import extract_user_handle_from_escaped_tag
        self.assertIsNone(extract_user_handle_from_escaped_tag('something else'))

    def test_user_id_extracted_from_command(self):
        from logs.slack_utils import extract_user_handle_from_escaped_tag
        id = extract_user_handle_from_escaped_tag('<@U1234|andyP>')

        self.assertEqual(id, 'andyP')