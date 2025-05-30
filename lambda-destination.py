import json
from datetime import datetime
import boto3
import os

# Initialize DynamoDB client and table name
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('DESTINATION_TABLE_NAME', 'poc-eventbridge-cross-region-destination_table')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    print(json.dumps(event, separators=(',', ':')))

    # Direct EventBridge invocation — top-level 'detail' key
    detail = event.get('detail', {})
    
    # Append a second timestamp
    detail['timestamp_destination_lambda'] = datetime.utcnow().isoformat() + "Z"

    # Validate presence of 'id' (partition key)
    message_id = detail.get('id')
    if not message_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing 'id' in event detail"})
        }

    # Store the event in DynamoDB
    try:
        table.put_item(Item=detail)
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"DynamoDB insert failed: {str(e)}"})
        }

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Event processed and stored", "id": message_id})
    }
