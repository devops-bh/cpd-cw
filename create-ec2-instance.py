# assuming I interpreted the coursework docs correctly, we need not implement the cost optimization 
# so this is just a regular EC2 instance rather than a spot instance (which tends to be cheaper)

# not sure if I'll need an elastic IP 
# I found it really helped during the Devops coursework though 
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/ec2-example-elastic-ip-addresses.html


import boto3
import base64
import os
import uuid
from dotenv import load_dotenv
load_dotenv()

with open('upload-images.py') as file:
    # Is it common to have a singleton module? 
    # wait, am I just using route here so I don't YET need to worry about assigning roles/groups security policies yet? 
    client = boto3.client(
        'ec2', region_name='us-east-1',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], # todo: use env vars
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'], # todo: use env vars
        aws_session_token=os.environ['AWS_SESSION_TOKEN'] # todo: use env vars
    )

    # todo: remember to append student id 
    # https://boto3.amazonaws.com/v1/documentation/api/1.9.42/guide/migrationec2.html?highlight=create_instances
    client.create_instances(ImageId='ami-'+str(uuid.uuid4()), MinCount=1, MaxCount=1,
                            UserData=base64.b64encode(file.read())
                            )

"""
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/create_instances.html
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html
https://cloudinit.readthedocs.io/en/latest/
"""