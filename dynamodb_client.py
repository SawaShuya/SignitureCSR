import boto3
from datetime import datetime

dynamodb = boto3.client('dynamodb')
table = "certificates"

def get_item(id):
    print(f"Start get item by ID : {id}")
    options = {
        "TableName" : table,
        "Key": {
            "id": {"S": id}
        }
    }

    try:
        response = dynamodb.get_item(**options)
        return {key: value['S'] for key, value in response['Item'].items()}

    except Exception as e:
        print(f"An error occurred: {e.response['Error']['Message']}")
        return None

def put_item(id, attribute_updates):
    print(f"Start put item by ID : {id}")
    options = {
        'TableName' : table,
        'Key' : { 'id' : {'S' : id }},
        'AttributeUpdates': attribute_updates
    }
    dynamodb.update_item(**options)



def add_info(id, serial_number):
    attribute_updates = {'serial': { 'Value': {'S' : str(serial_number) }}, 'signed_date': { 'Value' : { 'S' : datetime.utcnow().isoformat() }}}
    put_item(id, attribute_updates)
