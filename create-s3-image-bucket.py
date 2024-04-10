import boto3
import os
import uuid
import time
from dotenv import load_dotenv
load_dotenv()

client = boto3.client(
    's3',
    # does it make sense to do this? Given that this is going to be ran inside an EC2 instance, 
    # then shouldn't this be removed, and the auth will be done via AWS's relative auth services 
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], # todo: use env vars
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'], # todo: use env vars
    aws_session_token=os.environ['AWS_SESSION_TOKEN'] # todo: use env vars
)

# this will use the default region which is ? 
# general purpose buckets are likely going to be cheaper than directory buckets, where directory buckets are highly optimized 
# one of the main differences is how the objects are stored 
# I assume this defaults to a general purpose bucket? 
# How would I specify read/write permissions? 

response = client.create_bucket(
    # I think its possible to have the bucket name as just 
    # images-bucket if I somehow prevent the bucket from being availible to the public 
        Bucket='images-bucket-'+str(uuid.uuid4()),
)

"""
hacky way to give the bucket time to be created 
better ways of doing so may be to poll the head_object to determine if the bucket exists 
but I am assuming that the create_bucket function operates on eventual consistency in that 
the bucket will eventually be created, meaning that even without async code, the 
following code will still be called before the bucket is actually created
I've seen other APIs use a callback URL (webhook) for this 
"""
#time.sleep(60)
# I briefly considered putting the Queue template file upload code here, 
# but I had already created the bucket, so I guess this is since I'm too lazy to delete resources & repeat the processes 

