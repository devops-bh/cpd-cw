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

with open('upload-images.py', 'rb') as file:
    # Is it common to have a singleton module? 
    # wait, am I just using route here so I don't YET need to worry about assigning roles/groups security policies yet? 
    # https://hackernoon.com/resolving-typeerror-a-bytes-like-object-is-required-not-str-in-python
    client = boto3.client(
        'ec2', region_name='us-east-1',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], # todo: use env vars
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'], # todo: use env vars
        aws_session_token=os.environ['AWS_SESSION_TOKEN'] # todo: use env vars
    )

    # todo: remember to append student id 
    # https://boto3.amazonaws.com/v1/documentation/api/1.9.42/guide/migrationec2.html?highlight=create_instances
    """
    # this link implies that the newer method is create_instances, but despite referencing boto3 & not boto, 
    # apparently the method does not exist :/ 
    # https://boto3.amazonaws.com/v1/documentation/api/1.9.42/guide/migrationec2.html?highlight=create_instances
    client.create_instances(ImageId='ami-'+str(uuid.uuid4()), MinCount=1, MaxCount=1,
                            UserData=base64.b64encode(file.read())
                            )
    """
    
    client.run_instances(ImageId='ami-08e4e35cccc6189f4', MinCount=1, MaxCount=1,
                        # originally I intended on trying to automate the execution of the python script 
                        # where 1 way would be injecting the bucket name, and env variables into the script 
                        # using the replace function, but ultimately figured I didn't have enough time 
                        # since I lost alot of time due my account being bugged & not letting me 
                        # ssh into ec2 instance, the deactivation & reactivation of the AWS account fixed this 
                       #     UserData=base64.b64encode(file.read()), KeyName='vockey'
                            )

"""
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/create_instances.html
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html
https://cloudinit.readthedocs.io/en/latest/
"""