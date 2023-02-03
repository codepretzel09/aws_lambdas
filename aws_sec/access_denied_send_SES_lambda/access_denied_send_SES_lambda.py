import boto3

def send_alert_email(event):
    ses = boto3.client('ses')
    response = ses.send_email(
        Source='sender@example.com',
        Destination={
            'ToAddresses': ['receiver@example.com']
        },
        Message={
            'Subject': {
                'Data': 'Access Denied Alert'
            },
            'Body': {
                'Text': {
                    'Data': 'An Access Denied event was detected in your AWS environment: \n\n' + str(event)
                }
            }
        }
    )

def lambda_handler(event, context):
    cloudtrail = boto3.client('cloudtrail')
    response = cloudtrail.lookup_events(
        LookupAttributes=[
            {
                'AttributeKey': 'EventName',
                'AttributeValue': 'AccessDenied'
            },
        ]
    )
    for event in response['Events']:
        send_alert_email(event)
