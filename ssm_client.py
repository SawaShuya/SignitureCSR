import os
import json
import boto3

ssm = boto3.client('ssm')

# Call restored parameters in System Manager Prameter Store
def get_params(*args):
    if len(args) == 0:
        raise ValueError("Parametar name error. Please set parameter names.")
    
    print(f"GET Params from SSM Parameter Store: {args}")
    response = ssm.get_parameters(
        Names=list(args),
        WithDecryption=True
    )

    if len(args) > 1:
        values = []
        for name in list(args):
            value = next((d["Value"] for d in response['Parameters'] if d["Name"] == name), None)
            values.append(value)
        return values

    else:
        value = response['Parameters'][0]["Value"]
        return value


def start_automation(id, email, comment, subject):
    ssm.start_automation_execution(
        DocumentName='AutomationApproval',
        Parameters={
            "RequestID": [ id ],
            "RequesterComment": [ email ],
            "RequesterEmail":  [ comment ],
            "CSRContent": [ subject ]
        }
    )
