import boto3

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
        print(event)
