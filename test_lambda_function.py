import unittest
from unittest.mock import Mock, patch
from lambda_function import (
    lambda_handler,
    generate_recommendations,
    save_recommendations,
)

class TestLambdaFunction(unittest.TestCase):

    @patch('lambda_function.requests.get')
    @patch('lambda_function.recommendations_table.put_item')
    def test_lambda_handler_success(self, mock_put_item, mock_requests_get):
        # Mock the response from the health records API
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = {
            'weight': 70,
            'height': 170,
            'bloodPressure': 120,
        }

        # Mock the DynamoDB put_item response
        mock_put_item.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}

        # Create a sample event
        event = {'pathParameters': {'recordId': '123'}}

        # Call the Lambda handler
        result = lambda_handler(event, None)

        # Assert the expected DynamoDB put_item call
        mock_put_item.assert_called_with(
            Item={'recordId': '123', 'recommendations': '{"weight": "Maintain a balanced diet and exercise regularly for overall well-being.", "height": "Maintain a healthy lifestyle to support overall health and well-being.", "blood_pressure": "Maintain a low-sodium diet and engage in regular exercise to support healthy blood pressure."}'}
        )

        # Assert the expected response
        expected_response = {
            'weight': 'Maintain a balanced diet and exercise regularly for overall well-being.',
            'height': 'Maintain a healthy lifestyle to support overall health and well-being.',
            'blood_pressure': 'Maintain a low-sodium diet and engage in regular exercise to support healthy blood pressure.'
        }
        self.assertEqual(result, expected_response)

    # Add similar test cases for other functions

if __name__ == '__main__':
    unittest.main()
