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
    table_name = 'FaceAnalyses'
    # these (file_name) would come from the SQS queue 
    bucket_name = "images-bucket-5810aa5b-a4e8-41e3-bbe4-0d389d738f14"
    file_name = "image1.jpg"
    rekognition_response = rekognition_client.detect_faces(
        Image={"S3Object": {"Bucket": bucket_name, "Name": "images/"+file_name}},
        Attributes=["ALL"]) # I think I should've just done ["FaceDetails"]
        
    rekognition_labels_response = rekognition_client.detect_labels(
             Image={"S3Object": {"Bucket": bucket_name, "Name": "images/"+file_name}}, 
             MaxLabels=5
    )
    labels_list = [label['Name'] for label in rekognition_labels_response['Labels']]
    # the coursework spec doesnt specify how the labels should be stored 
    labels = ", ".join(labels_list, ",")
        
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
    face_analyses_and_labels = []
    face_analyses_and_labels.append({"ImageName": {"S": file_name}})
    face_analyses_and_labels.append({"labels": {"S": labels}})
    for face in rekognition_response['FaceDetails']:
        face_analysis = {}
        for emotion in face["Emotions"]:
            print(emotion)
            # python doesn't seem to have switch statements 
            if emotion["Type"].upper() == "Calm".upper():
                face_analysis.update({"CalmConfidenceScore": {"S": str(emotion["Confidence"])}})
            if emotion["Type"].upper() == "Happy".upper():
                face_analysis.update({"HappyConfidenceScore": {"S": str(emotion["Confidence"])}})
            if emotion["Type"].upper() == "Angry".upper():
                face_analysis.update({"AngryConfidenceScore": {"S": str(emotion["Confidence"])}})
            if emotion["Type"].upper() == "Frustrated".upper():
                face_analysis.update({"FrustratedConfidenceScore": {"S": str(emotion["Confidence"])}})
        face_analyses_and_labels.append(face_analysis)
        face_analyses_and_labels.append({"labels": {"S": "labels"}})
        
    print(face_analyses_and_labels)
    # Prepare the batch write request
    request_items = {
        str(table_name): [
            {
                'PutRequest': {
                    'Item': face_analysis
                }
            } for face_analysis in face_analyses_and_labels
        ]
    }
    print(request_items)
    # Perform the batch write operation
    dynamodb_response = dynamodb_client.batch_write_item(RequestItems=request_items)
    
    # Print the response
    print(dynamodb_response)
    
