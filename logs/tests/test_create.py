from unittest import TestCase
from unittest.mock import MagicMock, patch

import sys

class TestCreate(TestCase):

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
        &command=/log\
        &text=2%20hours%20on%20slack\
        &response_url=https://hooks.slack.com/commands/1234/5678\
        &trigger_id=13345224609.738474920.8088930838d88f008e0"

    def setUp(self):
        boto3_mock = MagicMock()
        self.put_item_mock = boto3_mock.resource.return_value.Table.return_value.put_item
        
        self.uuid_mock = MagicMock()
        self.uuid_mock.uuid1.return_value = 1234

        self.time_mock = MagicMock()
        self.time_mock.time.return_value = 1

        sys.modules['boto3'] = boto3_mock
        sys.modules['uuid'] = self.uuid_mock
        sys.modules['time'] = self.time_mock

    def test_minutes_extracted_from_command(self):
        """
        Minutes should be parsed in a number of formats from the slack command
        """
        from logs.create import parse_minutes

        for command, expectation in [
            ("1min", "1"),
            ("1 min", "1"),
            ("10 mins", "10"),
            ("1000minutes", "1000"),
            ("10 mins on another 10 things", "10"),
            ("2 hours on blah", "120"),
            ("2h on blah", "120"),
            ("3 hrs on blah", "180")]:
            with self.subTest(command=command, expected_minutes=expectation):
                self.assertEqual(parse_minutes(command), expectation)

    def test_project_extracted_from_command(self):
        """
        Projects should be parsed as the final text following the first 'on'
        """
        from logs.create import parse_project

        for command, expectation in [
            ("1 hour on this", "this"),
            ("1 hour on this multiple word example", "this multiple word example"),
            ("1 hour on \"this\"", "this"),
            ("1 hour on 'this'", "this")]:
            with self.subTest(command=command, expected_minutes=expectation):
                self.assertEqual(parse_project(command), expectation)

    def test_no_match_returns_none(self):
        """
        When regex match fails, return None
        """
        from logs.create import parse_minutes, parse_project

        self.assertIsNone(parse_minutes(''))
        self.assertIsNone(parse_minutes('10'))
        self.assertIsNone(parse_project(''))

    @patch('utils.slack_utils.is_slack_event')
    def test_create_returns_200_on_success(self, mock_slack_utils):
        mock_slack_utils.return_value = True
        from logs.create import create

        with patch.dict('os.environ', {'DYNAMODB_LOG_TABLE': 'some-table-name'}):
            response = create({'body': self.slack_example}, {})

        self.assertEqual(200, response['statusCode'])
        self.put_item_mock.assert_called_once_with(Item={
            'id': "1234",
            'user_id': "U2147483697",
            'command': "2 hours on slack",
            'minutes': "120",
            'project': "slack",
            'createdAt': 1000,
        })

    @patch.dict('os.environ', {'SLACK_SIGNING_SECRET': 'mysecret'})
    def test_create_returns_400_on_missing_time(self):
        from logs.create import create

        with patch.dict('os.environ', {'DYNAMODB_LOG_TABLE': 'some-table-name'}):
            response = create({'body': self.slack_example.replace('2%20hours','hour')}, {})

        self.assertEqual(400, response['statusCode'])
        self.put_item_mock.assert_not_called()

    @patch.dict('os.environ', {'SLACK_SIGNING_SECRET': 'mysecret'})
    def test_create_returns_400_on_missing_project(self):
        from logs.create import create

        with patch.dict('os.environ', {'DYNAMODB_LOG_TABLE': 'some-table-name'}):
            response = create({'body': self.slack_example.replace('%20on%20slack','')}, {})

        self.assertEqual(400, response['statusCode'])
        self.put_item_mock.assert_not_called()
