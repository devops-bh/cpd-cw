from dotenv import load_dotenv
load_dotenv()
import os

load_dotenv()
print(os.environ['AWS_SESSION_TOKEN'])

import boto3
import base64

client = boto3.client(
    'ec2', region_name='us-east-1',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], # todo: use env vars
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'], # todo: use env vars
    aws_session_token=os.environ['AWS_SESSION_TOKEN'] # todo: use env vars
)

help(client)

# don't know hwo to print the b64 encoded file as a string but it doesn't matter
"""
with open('upload-images.py') as file: 
    print(str(file.read()))
    print(str(base64.b64encode(file.read())))
"""

