from unittest import TestCase

from decimal import Decimal

class TestDBConversion(TestCase):
    example_response = {'Items': [{'project': 'slack', 'createdAt': Decimal('1546960691250'), 'user_id': 'UC7J5N60Z', 'id': 'sgsdfsdfg-1358-11e9-934f-f62b13c419f4', 'minutes': '4', 'command': '4 mins on slack'}, {'project': 'slack', 'createdAt': Decimal('1546960691216'), 'user_id': 'UC7J5N60Z', 'id': '9c522eaa-1358-11e9-934f-f62b13c419f4', 'minutes': '2', 'command': '2 mins on slack'}, {'project': 'slack create', 'createdAt': Decimal('1546949987986'), 'user_id': 'UC7J5N60Z', 'id': 'b0b2eb96-133f-11e9-992c-d2b4fce47cc6', 'minutes': '1', 'command': '1 min on slack create'}], 'Count': 2, 'ScannedCount': 10, 'ResponseMetadata': {'RequestId': 'V9H13MEGQJ6E4KEPT845HHS69RVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Tue, 08 Jan 2019 15:35:51 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '436', 'connection': 'keep-alive', 'x-amzn-requestid': 'V9H13MEGQJ6E4KEPT845HHS69RVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '3121682291'}, 'RetryAttempts': 0}}

    def test_conversion_to_slack_response(self):
        from logs.dynamodb_utils import group_db_response_by_date_project

        self.assertEqual(group_db_response_by_date_project(self.example_response), {'01/08/19': {'slack': 6, 'slack create': 1}})

