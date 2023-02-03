import boto3
from datetime import datetime, timedelta

# Set up the SSO and SES clients
sso = boto3.client('sso')
ses = boto3.client('ses')

# Set the time range for the SSO connections to retrieve (e.g. the last 24 hours)
start_time = datetime.utcnow() - timedelta(hours=24)
end_time = datetime.utcnow()

# Retrieve the SSO connections
response = sso.describe_sso_instances(
    StartTime=start_time,
    EndTime=end_time
)

# Format the connections information into a readable format
connections = response['InstanceMetadataList']
table_rows = []
for connection in connections:
    table_rows.append([
        connection['CreatedDate'],
        connection['PrincipalName'],
        connection['ApplicationId'],
        connection['ApplicationInstanceId']
    ])

# Set the email parameters
to_email = 'user@example.com'  # The recipient of the email
subject = 'Recent SSO Connections'
body = '''
<p>Here are the recent sso connections </p>

'''


