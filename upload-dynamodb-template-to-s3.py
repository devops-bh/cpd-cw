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

# not entirely sure how I actually have AWS execute a YML file, 
# but the most simplest & quickest way is to point AWS to a template which is stored in an S3 bucket   
# You'd likely have different buckets but I am just going to reuse the images bucket for simplicity 
# also, rather than hardcoding bucket names, I could possibly do something like (JS) buckets.foreach(bucket => {if bucket.name.includes('images')} )
bucket_name = "images-bucket-540d97a4-b538-4e96-bb40-172e3efa7357"
# I don't think DynamoDB requires you to define the loose equivalent of columns up front, 
# instead you only seem to need the partition name 
# but I wanted to try defining the columns up first 
code_path = f"dynamodb-table-template.yml"
code_key = f"dynamodb-table-template.yml" 
client.upload_file(code_path, bucket_name, code_key)

