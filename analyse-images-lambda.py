import json
import boto3

rekognition_client = boto3.client('rekognition')
dynamodb_client = boto3.client('dynamodb')
s3 = boto3.client('s3')
def list_image_items(bucket_name):
    images = []
    response = s3.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        for item in response['Contents']:
            if "image" in item['Key']:
                images.append(item['Key'])
    return images

# I probably should had realized in advance that by batching these operations, I'm spamming myself with emails 
def lambda_handler(event, content):
    table_name = 'FaceAnalysisStack-FaceAnalysisDB-V22UQZE8OOSQ'
    bucket_name = "images-bucket-5810aa5b-a4e8-41e3-bbe4-0d389d738f14"
    requests = []

    for image_path in list_image_items(bucket_name):
        file_name = image_path.split('/')[-1] 
        # I had to increase the timeout period for the lambda function 
        # suggesting that these requests should be done before this stage in the code 
        # I'm not sure if multithreading or async await code is allowed in a lambda, 
        # but may be worth investigating https://docs.aws.amazon.com/lambda/latest/dg/invocation-async.html 
        # and perhaps step functions 
        rekognition_response = rekognition_client.detect_faces(
            Image={"S3Object": {"Bucket": bucket_name, "Name": image_path}},
            Attributes=["ALL"])

        rekognition_labels_response = rekognition_client.detect_labels(
            Image={"S3Object": {"Bucket": bucket_name, "Name": image_path}}, 
            MaxLabels=5
        )
        labels_list = [label['Name'] for label in rekognition_labels_response['Labels']]
        labels = ", ".join(labels_list)

        # Initialize the item for DynamoDB
        item = {
            "ImageName": {"S": file_name},
            "calmConfidenceScore": {"S": ""},
            "happyConfidenceScore": {"S": ""},
            "angryConfidenceScore": {"S": ""},
            "frustratedConfidenceScore": {"S": ""},
            "labels": {"S": labels}
        }

        for face in rekognition_response['FaceDetails']:
            for emotion in face["Emotions"]:
                emotion_type = emotion["Type"].upper()
                if emotion_type == "CALM":
                    item["calmConfidenceScore"]["S"] = str(emotion["Confidence"])
                elif emotion_type == "HAPPY":
                    item["happyConfidenceScore"]["S"] = str(emotion["Confidence"])
                elif emotion_type == "ANGRY":
                    item["angryConfidenceScore"]["S"] = str(emotion["Confidence"])
                elif emotion_type == "FRUSTRATED":
                    item["frustratedConfidenceScore"]["S"] = str(emotion["Confidence"])

        # Add the item to the batch requests
        requests.append({
            'PutRequest': {
                'Item': item
            }
        })

        dynamodb_client.batch_write_item(
            RequestItems={
                table_name: requests
            }
        )
        requests = [] 

    return "Batch insertion completed."