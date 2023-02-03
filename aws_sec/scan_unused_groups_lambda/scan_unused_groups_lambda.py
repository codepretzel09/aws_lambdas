import boto3

# Create an IAM client
iam = boto3.client('iam')

def lambda_handler(event, context):
    # List all IAM groups
    groups = iam.list_groups()['Groups']

    # Create an empty list to store unused groups
    unused_groups = []

    # Iterate over the list of groups
    for group in groups:
        # Get the group name
        group_name = group['GroupName']

        # Get the list of users in the group
        users = iam.get_group(GroupName=group_name)['Users']

        # If the group has no users, add it to the list of unused groups
        if len(users) == 0:
            unused_groups.append(group_name)

    # Return the list of unused groups
    return unused_groups
