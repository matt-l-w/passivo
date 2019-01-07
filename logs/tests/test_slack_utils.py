from unittest import TestCase

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
        