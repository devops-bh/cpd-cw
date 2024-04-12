# this runs inside the ec2 instace created by create-ec2-instance.py
import boto3
import os 
from botocore.exceptions import ClientError
import time
from dotenv import load_dotenv
load_dotenv()

# since this code is running locally, and presumably as a form of root (bad idea), I don't think it needs the auth stuff
# nevermind, I think either i'd need to do AWS configurations (e.g. IAM and/or maybe VPC)
# or I'd need to do the less secure option (which yes I'm doing) due to time constraints 
# is copying the .env file to the remote instance (in the real world, you'd have different env files when doing this)
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

# ideally this could use the os + path packages to figure out number of images in file 
#bucket_name = "images-bucket-a8b52607-050f-4b06-bf98-9c10814e098a"
#bucket_name = "images-bucket-5810aa5b-a4e8-41e3-bbe4-0d389d738f14"
bucket_name = "images-bucket-540d97a4-b538-4e96-bb40-172e3efa7357"
# I may not even need this for loop, & maybe be able to upload the entire folder but this seems simpler 
for image_index in range(1, 6):
    time.sleep(10)
    # I assume asyncio could do this asynchronously if there were a large volume of images 
    image_path = f"images/image{image_index}.jpg"
    image_key = f"images/image{image_index}.jpg" # This is the 'Key' parameter
    client.upload_file(image_path, bucket_name, image_key)

# Specify your bucket name and the path to the image


