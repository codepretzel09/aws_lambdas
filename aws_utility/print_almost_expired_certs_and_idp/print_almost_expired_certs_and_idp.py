import boto3
from datetime import datetime, timedelta

# Set up the client for the AWS Identity and Access Management (IAM) service
iam_client = boto3.client('iam')

def lambda_handler(event, context):
    # Get the current time
    now = datetime.now()

    # Set the threshold for expiration to 30 days from now
    expiration_threshold = now + timedelta(days=30)

    # Get a list of all certificates that are about to expire in AWS
    certificates = iam_client.list_server_certificates()

    # Iterate through the list of certificates and print their expiration dates if they will expire within the next 30 days
    for certificate in certificates['ServerCertificateMetadataList']:
        expiration = certificate['Expiration']
        if expiration <= expiration_threshold:
            print(f"Certificate with name {certificate['ServerCertificateName']} will expire on {expiration}")

    # Get a list of all identity providers that are about to expire in AWS
    identity_providers = iam_client.list_identity_providers()

    # Iterate through the list of identity providers and print their expiration dates if they will expire within the next 30 days
    for identity_provider in identity_providers['Providers']:
        expiration = identity_provider['Expiration']
        if expiration <= expiration_threshold:
            print(f"Identity provider with name {identity_provider['ProviderName']} will expire on {expiration}")
