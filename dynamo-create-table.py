import boto3

# Região do destino (Oregon)
region = "us-west-2"
table_name = "poc-eventbridge-cross-region-destination_table"

# Inicializa cliente do DynamoDB para região de destino
dynamodb = boto3.client("dynamodb", region_name=region)

def create_table():
    try:
        response = dynamodb.create_table(
            TableName=table_name,
            AttributeDefinitions=[
                {
                    "AttributeName": "id",
                    "AttributeType": "S"
                }
            ],
            KeySchema=[
                {
                    "AttributeName": "id",
                    "KeyType": "HASH"
                }
            ],
            BillingMode="PAY_PER_REQUEST",  # Modo serverless (on-demand)
            Tags=[
                {
                    "Key": "Project",
                    "Value": "poc-eventbridge-cross-region"
                }
            ]
        )
        print(f"Table creation initiated. Table ARN: {response['TableDescription']['TableArn']}")
    except dynamodb.exceptions.ResourceInUseException:
        print(f"Table '{table_name}' already exists.")
    except Exception as e:
        print(f"Error creating table: {e}")

if __name__ == "__main__":
    create_table()
