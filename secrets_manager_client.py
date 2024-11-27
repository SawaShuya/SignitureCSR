import ast
import boto3
import json
from botocore.exceptions import ClientError

def get_secret(key):
    secret_name = "lambda/RootCAKey"
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager')
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e


    secret_data = get_secret_value_response['SecretString'].replace("\\\\", "\\")
    secret = json.loads(secret_data)

    return secret[key]

    
