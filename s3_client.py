import boto3

bucket_name = "certificate-management-bucket"
s3 = boto3.client('s3')


def get_object(object_key):
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    return response['Body'].read()

def upload_file(local_file, key):
    s3.upload_file(local_file, bucket_name, key)
    print(f"Successfully uploaded {local_file} to s3://{bucket_name}/{key}")
