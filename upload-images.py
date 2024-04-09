# this runs inside the ec2 instace created by create-ec2-instance.py
import boto3
import os 
import time
from dotenv import load_dotenv
load_dotenv()

# since this code is running locally, and presumably as a form of root (bad idea), I don't think it needs the auth stuff
client = boto3.client(
    's3',
    # does it make sense to do this? Given that this is going to be ran inside an EC2 instance, 
    # then shouldn't this be removed, and the auth will be done via AWS's relative auth services 
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], # todo: use env vars
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'], # todo: use env vars
    aws_session_token=os.environ['AWS_SESSION_TOKEN'] # todo: use env vars
)

# append student id 
# could maybe store uuids in an env or a JSON file? 
bucket = '/images-bucket-a8b52607-050f-4b06-bf98-9c10814e098a' 

# ideally this could use the os + path packages to figure out number of images in file 
for image_index in range(1, 5):
    time.sleep(10)
    file_name = 'image'+str(i)+".jpg" # is file_name the name & path? 
    key_name = 'image'+str(image_index)
    # I assume asyncio could do this asynchronously if there were a large volume of images 
    client.upload_file('./images/' + file_name, bucket, key_name)