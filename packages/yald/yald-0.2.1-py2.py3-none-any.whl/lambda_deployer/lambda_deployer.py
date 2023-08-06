from pprint import pprint
from typing import Dict, Optional, TypedDict

import boto3


class Credentials(TypedDict):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str


def assume_role(role_arn) -> Credentials:
    client = boto3.client('sts')
    response = client.assume_role(
        RoleArn=role_arn,
        RoleSessionName='lambda_deployer'
    )

    credentials = response['Credentials']
    key_id = credentials['AccessKeyId']
    secret_key = credentials['SecretAccessKey']
    token = credentials['SessionToken']
    return {
        'aws_access_key_id': key_id,
        'aws_secret_access_key': secret_key,
        'aws_session_token': token
    }


def upload_to_s3(filename: str, bucket: str, key: str, credentials: Optional[Credentials] = None):
    kw = {} if credentials is None else credentials
    s3_client = boto3.client('s3', **kw)
    s3_client.upload_file(filename, bucket, key)


def update_lambda(
        function_name,
        filename,
        bucket=None,
        key=None,
        credentials: Optional[Credentials] = None,
        env: Dict[str, str] = {}
):
    if bucket is None:
        code = {
            'ZipFile': open(filename, 'rb').read()
        }
    else:
        upload_to_s3(filename, bucket, key, credentials)
        code = {
            'S3Bucket': bucket,
            'S3Key': key
        }

    kw = {} if credentials is None else credentials
    client = boto3.client('lambda', **kw)
    if env:
        print('Updating function environment...')
        response = client.update_function_configuration(
            FunctionName=function_name,
            Environment={
                'Variables': env
            }
        )
        pprint(response)

    print('Updating function code...')
    response = client.update_function_code(
        FunctionName=function_name,
        Publish=True,
        **code
    )
    pprint(response)
