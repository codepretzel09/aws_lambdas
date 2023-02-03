import boto3

# Enter the email address to send the alert to
email_address = 'alerts@example.com'

def lambda_handler(event, context):
    # Get the S3 client
    s3 = boto3.client('s3')

    # Check if the deleted object was a file
    if event['Records'][0]['eventName'] == 'ObjectRemoved:Delete':
        # Get the name of the deleted object
        object_name = event['Records'][0]['s3']['object']['key']

        # Get the name of the bucket that the object was deleted from
        bucket_name = event['Records'][0]['s3']['bucket']['name']

        # Compose the email message
        message = f'An object was deleted from the {bucket_name} bucket:\n\n'
        message += f'Object name: {object_name}\n\n'
        message += f'Event: {event}'

        # Send the email using SES
        ses = boto3.client('ses')
        response = ses.send_email(
            Source=email_address,
            Destination={
                'ToAddresses': [email_address]
            },
            Message={
                'Subject': {
                    'Data': f'Object deleted from {bucket_name}'
                },
                'Body': {
                    'Text': {
                        'Data': message
                    }
                }
            }
        )

        return response
