import os
import json

import dynamodb_client
import secrets_manager_client
import s3_client
import signiture
import file_utils
import mailing


def lambda_handler(event, context):
    id = event["id"]
    item = dynamodb_client.get_item(id)
    rootca_secret = secrets_manager_client.get_secret('RootCAKey')
    rootca_cert = s3_client.get_object("intermediate-certificate/RootCA.crt")
    # rootca_secret = "-----BEGIN PRIVATE KEY-----\n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\n5UYgPymABbsBmpyVr9YxybIhi4Ni4Q==\n-----END PRIVATE KEY-----"
    signed_cert, serial_number = signiture.exec(item["csrContent"], rootca_cert, rootca_secret)

    dynamodb_client.add_info(id, serial_number)

    tmp_file_path = "/tmp/certs"
    os.mkdir(tmp_file_path)
    file_utils.write_file(rootca_cert.decode(), f"{tmp_file_path}/rootca-cert.crt")
    file_utils.write_file(signed_cert.decode(), f"{tmp_file_path}/signed-cert.crt")
    file_utils.create_zip(tmp_file_path)

    s3_client.upload_file(f"{tmp_file_path}/signed-cert.crt",f"signed-certificate/{id}/signed-cert.crt")
    mailing.send(id, item["email"],"/tmp/certs.zip")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
