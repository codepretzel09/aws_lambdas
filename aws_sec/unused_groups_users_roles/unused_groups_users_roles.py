import boto3

# Set the AWS region you want to use
REGION = 'us-east-1'

# Create a client for the IAM service
iam_client = boto3.client('iam', region_name=REGION)

# Get a list of all IAM groups
groups = iam_client.list_groups()

# Iterate over the groups and print the group name and ARN
for group in groups['Groups']:
    group_name = group['GroupName']
    group_arn = group['Arn']

    # Check if the group has any attached policies
    policies = iam_client.list_attached_group_policies(GroupName=group_name)

    # If the group does not have any attached policies, it is considered unused
    if len(policies['AttachedPolicies']) == 0:
        print(f'Unused group: {group_name} ({group_arn})')

# Get a list of all IAM roles
roles = iam_client.list_roles()

# Iterate over the roles and print the role name and ARN
for role in roles['Roles']:
    role_name = role['RoleName']
    role_arn = role['Arn']

    # Check if the role has any attached policies
    policies = iam_client.list_attached_role_policies(RoleName=role_name)

    # If the role does not have any attached policies, it is considered unused
    if len(policies['AttachedPolicies']) == 0:
        print(f'Unused role: {role_name} ({role_arn})')

# Get a list of all IAM users
users = iam_client.list_users()

# Iterate over the users and print the user name and ARN
for user in users['Users']:
    user_name = user['UserName']
    user_arn = user['Arn']

    # Check if the user has any attached policies
    policies = iam_client.list_attached_user_policies(UserName=user_name)

    # If the user does not have any attached policies, it is considered unused
    if len(policies['AttachedPolicies']) == 0:
        print(f'Unused user: {user_name} ({user_arn})')
