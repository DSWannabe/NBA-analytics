import boto3
import json
from decimal import Decimal
from botocore.exceptions import ClientError

def convert_floats_to_decimal(obj):
    """Recursively convert floats to Decimal in a JSON object."""
    if isinstance(obj, float):
        return Decimal(str(obj))
    elif isinstance(obj, dict):
        return {k: convert_floats_to_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_floats_to_decimal(item) for item in obj]
    return obj

def upload_jsonl_to_dynamodb(jsonl_file_path, table_name, region_name='us-east-1'):
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb', region_name=region_name)
    table = dynamodb.Table(table_name)

    # Read JSONL file and upload each line
    with open(jsonl_file_path, 'r') as file:
        for line in file:
            try:
                # Parse each line as a JSON object
                item = json.loads(line.strip())

                # Convert any float values to Decimal
                item = convert_floats_to_decimal(item)

                # Put item into DynamoDB table
                table.put_item(Item=item)
                print(f"Successfully uploaded item: {item}")

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON line: {line.strip()} - {e}")
            except ClientError as e:
                print(f"Error uploading to DynamoDB: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

if __name__ == "__main__":
    # Specify your file path, table name, and region
    jsonl_file_path = '/home/anhtupham99/NBA-analytics/data/nba_players_seasonal_stats.jsonl'  # Path to your JSONL file
    table_name = 'NBA'    # Your DynamoDB table name
    region_name = 'us-east-1'       # Your AWS region

    upload_jsonl_to_dynamodb(jsonl_file_path, table_name, region_name)