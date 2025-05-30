import json
import uuid
from datetime import datetime
import boto3
import os

# Initialize the EventBridge client
eventbridge = boto3.client('events')

# Event bus name from environment variable or fallback default
EVENT_BUS_NAME = os.environ.get('EVENT_BUS_NAME', 'poc-eventbridge-cross-region-source-bus')

def lambda_handler(event, context):
    print("Raw event received:", json.dumps(event, separators=(',', ':')))

    # Generate a unique ID and source timestamp
    message_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + "Z"

    # Construct the enriched event with metadata and full incoming request
    enriched_event = {
        "id": message_id,
        "timestamp_source_lambda": timestamp,
        "request": event  # When Lambda Proxy Integration is enabled, this includes body, headers, path, method, etc.
    }

    # Publish the event to EventBridge
    try:
        response = eventbridge.put_events(
            Entries=[
                {
                    'Source': 'poc.eventbridge.crossregion',
                    'DetailType': 'message-event',
                    'Detail': json.dumps(enriched_event),
                    'EventBusName': EVENT_BUS_NAME
                }
            ]
        )
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Failed to put event: {str(e)}"})
        }

    # Return the generated event ID
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Event published successfully",
            "id": message_id
        })
    }
