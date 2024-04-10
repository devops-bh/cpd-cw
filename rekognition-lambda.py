import json
import boto3

# so by putting these here, do they essentially act like a singleton
# is a lambda function something which spawns its own thread or process for its code?
# i get what lambda is at a high level, but not sure what it is under the hood
# regardless, does putting these connections outside the lambda definition
# mean that the same connection is reused (kind of like a singleton?)
rekognition_client = boto3.client('rekognition')
dynamodb_client = boto3.client('dynamodb')


def lambda_handler(event, content):
    # Specify the table name
    table_name = 'FaceAnalysis'
    # these (file_name) would come from the SQS queue 
    bucket_name = "images-bucket-5810aa5b-a4e8-41e3-bbe4-0d389d738f14"
    file_name = "images/image1.jpg"
    rekognition_response = rekognition_client.detect_faces(
        Image={"S3Object": {"Bucket": bucket_name, "Name": file_name}},
        Attributes=["ALL"])
    """
    {'Type': 'HAPPY', 'Confidence': 98.046875}
    {'Type': 'SURPRISED', 'Confidence': 0.16510486602783203}
    {'Type': 'CALM', 'Confidence': 0.11110305786132812}
    {'Type': 'CONFUSED', 'Confidence': 0.0038802623748779297}
    {'Type': 'DISGUSTED', 'Confidence': 1.7881393432617188e-05}
    Wasn't sure whether to consider confidence store as a string or a number  
    I'd assume that Dynamodb has support for scientific numbers but to be on the 
    safe side I decided just to use a String (S) instead of Number (N) for the 
    attribute type
    I recall reading something like numbers are converted to strings anyway
    {'Type': 'ANGRY', 'Confidence': 5.9604644775390625e-06}
    {'Type': 'FEAR', 'Confidence': 0.0}
    {'Type': 'SAD', 'Confidence': 0.0}
    """
    face_analysises = []
    for face in rekognition_response['FaceDetails']:
        face_analysis = {}
        for emotion in face["Emotions"]:
            print(emotion)
            # python doesn't seem to have switch statements 
            if emotion["Type"].upper() == "Calm".upper():
                face_analysis.update({"CalmConfidenceScore": str(emotion["Confidence"])})
            if emotion["Type"].upper() == "Happy".upper():
                face_analysis.update({"HappyConfidenceScore": str(emotion["Confidence"])})
            if emotion["Type"].upper() == "Angry".upper():
                face_analysis.update({"AngryConfidenceScore": str(emotion["Confidence"])})
            if emotion["Type"].upper() == "Frustrated".upper():
                face_analysis.update({"FrustratedConfidenceScore": str(emotion["Confidence"])})
        face_analysises.append(face_analysis)
        
    print(face_analysises)
    # Prepare the batch write request
    request_items = {
        table_name: [
            {
                'PutRequest': {
                    'Item': item
                }
            } for face_analysis in face_analysises
        ]
    }
    print(request_items)
    # Perform the batch write operation
    dynamodb_response = dynamodb_client.batch_write_item(RequestItems=request_items)
    
    # Print the response
    print(dynamodb_response)
    
   
    """
    # Specify the table name
    table_name = 'FaceAnalysis'
    # these (file_name) would come from the SQS queue 
    bucket_name = "images-bucket-5810aa5b-a4e8-41e3-bbe4-0d389d738f14"
    file_name = "images/image1.jpg"

    rekognition_response = client.detect_faces(
        Image={"S3Object": {"Bucket": bucket_name, "Name": file_name}},
        Attributes=["ALL"])

    for face in response["FaceDetails"]:
        face_analysis = {
            "ImageName": {"S": "example_image_name"},
            "calm": {"N": str(face["Emotions"]["")},
            "happy": {"N": "85"},
            "angry": {"N": "10"},
            "frustrated": {"N": "5"}
        }

    
    # Put the item into the table
    response = dynamodb_client.put_item(
        TableName=table_name,
        Item=item_example
    )
    
    # Print the response
    print(response)
    """
"""
# REFERENCE CODE: WILL DELETE WHEN NO LONGER NEEDED 
# not sure if I need to setup policies or if this uses the lab role 
# or if I need to use the secret key etc 
# or not, as access maybe provided due to resources being on the same "Hyperplane"?
rekognition_client = boto3.client("rekognition")
dynamodb_client = boto3.client("dynamodb")

def lambda_handler(event, content):
    # these (file_name) would come from the SQS queue 
    bucket_name = "images-bucket-5810aa5b-a4e8-41e3-bbe4-0d389d738f14"
    file_name = "images/image1.jpg"

    response = client.detect_faces(
        Image={"S3Object": {"Bucket": bucket_name, "Name": file_name}},
        Attributes=["ALL"])
    # just a reference as to how I'd access the data 
    for face in response["FaceDetails"]:
        #print(json.dumps(face, indent=4))
        for emotions in face["Emotions"]:
            print(emotion)
        
    # either here or in the for loop; update the DynamoDB 
    dynamodb.put_item(TableName='ImageName', Item={'fruitName':{'S':'Banana'},'key2':{'N':'value2'}})


"""