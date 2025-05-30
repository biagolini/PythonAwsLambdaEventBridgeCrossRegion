# AWS EventBridge Cross-Region Event Replication

This repository contains source code used in the tutorial **"Testing AWS EventBridge for Cross-Region Event Replication"**, available at:  
👉 [https://medium.com/@biagolini](https://medium.com/@biagolini)

## Overview

This proof-of-concept demonstrates how to use **Amazon EventBridge** to implement cross-region event forwarding between AWS services. The architecture leverages API Gateway, Lambda, EventBridge, and DynamoDB to build a fully serverless, decoupled, and geographically distributed event-driven workflow.

## Repository Contents

- `dynamo-create-table.py`  
  Python script to create the `destination_table` DynamoDB table in the target region (`us-west-2`).

- `lambda-destination.py`  
  Lambda function code deployed in the **destination region**. It receives events from EventBridge, appends a timestamp, and writes the result to DynamoDB.

- `lambda-source.py`  
  Lambda function code deployed in the **source region**. It enriches incoming payloads and publishes custom events to a regional EventBridge bus.

## More Information

For detailed architecture, setup steps, and execution flow, please refer to the full tutorial:  
[https://medium.com/@biagolini](https://medium.com/@biagolini)

