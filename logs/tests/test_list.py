from unittest import TestCase
from unittest.mock import MagicMock, patch

from decimal import Decimal
import sys

class TestList(TestCase):

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
        &command=/logs\
        &text=<@U1234|andyP>\
        &response_url=https://hooks.slack.com/commands/1234/5678\
        &trigger_id=13345224609.738474920.8088930838d88f008e0"

    return_example_success = {
        'Items':[
            {'keyA1':'valueA1', 'keyA2':'valueA2'},
            {'keyB1':'valueB1', 'keyB2':'valueB2'}
        ]
    }

    def setUp(self):
        self.boto3_mock = MagicMock()

        self.eq_mock = MagicMock()
        conditions_mock = MagicMock()
        conditions_mock.Attr.return_value.eq.return_value = self.eq_mock

        sys.modules['boto3'] = self.boto3_mock
        sys.modules['boto3.dynamodb.conditions'] = conditions_mock

    @patch('utils.slack_utils.is_slack_event')
    def test_returns_200_on_success(self, mock_is_slack_event):
        from logs.list import list
        mock_is_slack_event.return_value = True
        scan_mock = self.boto3_mock.resource.return_value.Table.return_value.scan
        scan_mock.return_value = self.return_example_success

        with patch.dict('os.environ', {'DYNAMODB_LOG_TABLE': 'some-table-name'}):
            response = list({'body': self.slack_example}, {})

        scan_mock.assert_called_once_with(FilterExpression=self.eq_mock)
        self.assertEqual(200, response['statusCode'])


    # @patch('utils.slack_utils.is_slack_event')
    # def test_returns_404_message_on_no_matching_items(self, mock_is_slack_event):
    #     from logs.list import list
    #     mock_is_slack_event.return_value = True
    #     self.scan_mock.return_value = {'Items':[]}

    #     with patch.dict('os.environ', {'DYNAMODB_LOG_TABLE': 'some-table-name'}):
    #         response = list({'body': self.slack_example}, {})

    #     self.scan_mock.assert_called_once_with(FilterExpression=self.eq_mock)
    #     self.assertEqual(404, response['statusCode'])
    #     self.assertEqual(f"I couldn't find any time logged for @andyP")

# class TestDBConversion(TestCase):
#     example_response = {'Items': [{'project': 'slack', 'createdAt': Decimal('1546960691216'), 'user_id': 'UC7J5N60Z', 'id': '9c522eaa-1358-11e9-934f-f62b13c419f4', 'minutes': '2', 'command': '2 mins on slack'}, {'project': 'slack create', 'createdAt': Decimal('1546949987986'), 'user_id': 'UC7J5N60Z', 'id': 'b0b2eb96-133f-11e9-992c-d2b4fce47cc6', 'minutes': '1', 'command': '1 min on slack create'}], 'Count': 2, 'ScannedCount': 10, 'ResponseMetadata': {'RequestId': 'V9H13MEGQJ6E4KEPT845HHS69RVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Tue, 08 Jan 2019 15:35:51 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '436', 'connection': 'keep-alive', 'x-amzn-requestid': 'V9H13MEGQJ6E4KEPT845HHS69RVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '3121682291'}, 'RetryAttempts': 0}}

#     def setUp(self):
#         sys.modules['boto3'] = MagicMock()
#         sys.modules['boto3.dynamodb.conditions'] = MagicMock()

#     def test_conversion_to_slack_response(self):
#         from logs.list import group_db_response_by_date_project

#         self.assertEqual(group_db_response_by_date_project(self.example_response), "2 minutes on 'slack' on \n1 minutes on 'slack create' on ")

