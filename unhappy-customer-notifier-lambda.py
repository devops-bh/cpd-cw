import json
import boto3

dynamo_streams_client = boto3.client('dynamodbstreams')
sns_client = boto3.client('sns')
def lambda_handler(event, context):
    """
    response = dynamo_streams_client.get_records(
        ShardIterator='string',
        Limit=123
    )
    json.dumps(response)
    """
    print(event)
    # coursework spec said "immediately email" but alternatively you could count the number of angry/frustrated customers etc 
    for record in event['Records']:
        item = record['dynamodb']['NewImage']
        print(item["ImageName"])
        print(item["angryConfidenceScore"])
        print(item["frustratedConfidenceScore"])
        angryConfidenceScore = float(item["angryConfidenceScore"]["S"])
        frustratedConfidenceScore = float(item["angryConfidenceScore"]["S"])
        wasAngry = angryConfidenceScore > 0.1
        wasFrustrated = frustratedConfidenceScore > 0.1 
        if (wasAngry or wasFrustrated):
        # I'd assume lambda functions allow you to provide HTML based email templates ? 
            email = "there was a" 
            if wasAngry:
                # pretty sure the values are strings but just to be certain 
                email += f"n angry ({str(item['angryConfidenceScore']["S"])})"
            if  wasFrustrated:
                # pretty sure the values are strings but just to be certain 
                email += f" frustrated ({str(item['frustratedConfidenceScore']["S"])})"
            email += " customer"
            response = sns_client.publish(
                TopicArn='arn:aws:sns:us-east-1:345427350292:UnhappyTopic',
                Message=f"{email}"
            ) 
    
        #return response

"""
# for testing (e.g. within the AWS lambda console)
{
 "Records": [
    {
      "eventID": "c4ca4238a0b923820dcc509a6f75849b",
      "eventName": "INSERT",
      "eventVersion": "1.1",
      "eventSource": "aws:dynamodb",
      "awsRegion": "us-east-1",
      "dynamodb": {
        "Keys": {
          "Id": {
            "N": "101"
          }
        },
        "NewImage": {
          "ImageName": {
            "S": "example_image.jpg"
          },
          "calmConfidenceScore": {
            "S": "0.9"
          },
          "happyConfidenceScore": {
            "S": "0.8"
          },
          "angryConfidenceScore": {
            "S": "0.1"
          },
          "frustratedConfidenceScore": {
            "S": "0.05"
          },
          "labels": {
            "S": "label1, label2"
          }
        },
        "ApproximateCreationDateTime": 1428537600,
        "SequenceNumber": "4421584500000000017450439091",
        "SizeBytes": 26,
        "StreamViewType": "KEYS_ONLY"
      },
      "eventSourceARN": "arn:aws:dynamodb:us-east-1:123456789012:table/ExampleTableWithStream/stream/2015-06-27T00:48:05.899"
    }
 ]
}


{
 "Records": [
    {
      "eventID": "c4ca4238a0b923820dcc509a6f75849b",
      "eventName": "INSERT",
      "eventVersion": "1.1",
      "eventSource": "aws:dynamodb",
      "awsRegion": "us-east-1",
      "dynamodb": {
        "Keys": {
          "Id": {
            "N": "101"
          }
        },
        "NewImage": {
          "ImageName": {
            "S": "example_image.jpg"
          },
          "calmConfidenceScore": {
            "S": "0.9"
          },
          "happyConfidenceScore": {
            "S": "0.8"
          },
          "angryConfidenceScore": {
            "S": "0.2"
          },
          "frustratedConfidenceScore": {
            "S": "0.2"
          },
          "labels": {
            "S": "label1, label2"
          }
        },
        "ApproximateCreationDateTime": 1428537600,
        "SequenceNumber": "4421584500000000017450439091",
        "SizeBytes": 26,
        "StreamViewType": "KEYS_ONLY"
      },
      "eventSourceARN": "arn:aws:dynamodb:us-east-1:123456789012:table/ExampleTableWithStream/stream/2015-06-27T00:48:05.899"
    }
 ]
}

"""