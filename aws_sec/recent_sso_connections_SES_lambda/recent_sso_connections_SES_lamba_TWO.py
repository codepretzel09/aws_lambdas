import boto3

def get_recent_sso_connections_and_email(days_ago=7):
    # Connect to SSO using boto3
    sso = boto3.client('sso')

    # Get a list of recent SSO connections
    connections = sso.list_account_roles(
        maxResults=100,
        filter="lastAuthenticatedTime>={}d".format(days_ago)
    )

    # Create the email body
    email_body = "Recent SSO connections:\n"
    for connection in connections:
        email_body += "- {}\n".format(connection)

    # Connect to SES using boto3
    ses = boto3.client('ses')

    # Send the email using SES
    ses.send_email(
        Source="your_email@example.com",
        Destination={
            "ToAddresses": ["recipient_email@example.com"]
        },
        Message={
            "Subject": {
                "Data": "Recent SSO Connections"
            },
            "Body": {
                "Text": {
                    "Data": email_body
                }
            }
        }
    )
