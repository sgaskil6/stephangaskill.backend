import json
import boto3
import os
from boto3.dynamodb.conditions import Key # This is used for the DynamoDB Update Table Resource
from moto import mock_dynamodb2
from visitCountLambda import lambda_handler

def aws_setup():
    # Mock AWS credentials
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AwS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

    # Database table name into env variable
    os.environ['databaseName'] = 'testing'

class TestLambdaDDB(unittest.TestCase):
    @mock_dynamodb2
    def test_handler(self):
        # Create dynamodb boto3 object
        dynamodb = boto3.client('dynamodb')
        # Get dynamodb table name from env
        ddbTableName = os.environ['databaseName']

        # Create mock table
        dynamodb.create_table(
            TableName = ddbTableName,
            BillingMode = 'PAY_PER_REQUEST',
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
            ],
            KeySchema = [
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                },
            ]
        )

        # Print Lambda response
        LambdaResponse = handler(0, 0)
        print("Lambda response: ", LambdaResponse)

        # Run unit test against Lambda status code
        self.assertEqual(200, LambdaResponse['statusCode'])

if __name__ == '__main__':
    aws_setup()
    unittest.main()