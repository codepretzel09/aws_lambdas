import json
import boto3

def lambda_handler(event, context):
    
    # Create an SNS client
    sns = boto3.client("sns")

    # Extracting the relevant data from the event
    principalId = event["detail"]["userIdentity"]["principalId"]
    eventName = event["detail"]["eventName"]
    sourceIPAddress = event["detail"]["sourceIPAddress"]
    eventSource = event["detail"]["eventSource"]
    accessKeyId_create = event["detail"]["responseElements"]["accessKey"]["accessKeyId"]
    accessKeyStatus = event["detail"]["responseElements"]["accessKey"]["status"]
    accessKeyCreateDate = event["detail"]["responseElements"]["accessKey"]["createDate"]
    
    message = (f"New access key created by: {principalId}\n"
               f"Event Name: {eventName}\n"
               f"sourceIPAddress: {sourceIPAddress}\n"
               f"eventSource: {eventSource}\n"
               f"Access Key ID (created): {accessKeyId_create}\n"
               f"Access Key Status: {accessKeyStatus}\n"
               f"Access Key Create Date: {accessKeyCreateDate}")
    # Printing the extracted data
    print(message)


    # Publish the message to the SNS topic
    sns.publish(TopicArn="arn:aws:sns:us-east-1:803775072478:new_key_created", Message=message)
