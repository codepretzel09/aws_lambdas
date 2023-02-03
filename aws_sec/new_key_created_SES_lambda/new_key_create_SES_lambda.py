import boto3

def lambda_handler(event, context):
    # Create an SES client
    ses = boto3.client('ses')

    # Retrieve the IAM key that was created
    key = event['detail']['key']

    # Send an email using SES to alert of the new key
    response = ses.send_email(
        Source='alerts@example.com',
        Destination={
            'ToAddresses': ['security@example.com']
        },
        Message={
            'Subject': {
                'Data': 'New IAM Key Created'
            },
            'Body': {
                'Text': {
                    'Data': f'A new IAM key was created with the ID {key}.'
                }
            }
        }
    )

    return response
