import boto3

def lambda_handler(event, context):
    # Set the time period for which you want to get recent access information
    time_period = 7200 # 2 hours
    
    # Get the current time
    current_time = int(time.time())
    
    # Create a boto3 client for AWS Identity and Access Management (IAM)
    iam_client = boto3.client('iam')
    
    # Get a list of all access keys for the current account
    response = iam_client.list_access_keys()
    access_keys = response['AccessKeyMetadata']
    
    # Iterate over the list of access keys and get the last used time for each key
    for key in access_keys:
        key_id = key['AccessKeyId']
        response = iam_client.get_access_key_last_used(AccessKeyId=key_id)
        last_used = response['AccessKeyLastUsed']['LastUsedDate']
        last_used_time = int(last_used.strftime('%s'))
        
        # Check if the key was used within the specified time period
        if (current_time - last_used_time) <= time_period:
            print(key_id + " was used within the last 2 hours")
