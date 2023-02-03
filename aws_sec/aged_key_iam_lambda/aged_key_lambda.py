import boto3

def lambda_handler(event, context):
    # Set the date that you want to consider as "aged"
    aged_date = "2020-01-01"

    # Create an IAM client
    iam = boto3.client('iam')

    # List the access keys for all IAM users
    response = iam.list_access_keys()

    # Iterate over the list of access keys
    for user in response['AccessKeyMetadata']:
        # Get the access key ID and the date it was last used
        key_id = user['AccessKeyId']
        last_used = user['LastUsedDate']

        # Check if the access key is aged (last used before the specified date)
        if last_used < aged_date:
            # Handle the aged access key (e.g. disable it, send a notification, etc.)
            pass
