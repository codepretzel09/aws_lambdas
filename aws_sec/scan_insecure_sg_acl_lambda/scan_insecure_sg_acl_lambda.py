import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Get a list of all security groups in the current region
    security_groups = ec2.describe_security_groups()['SecurityGroups']
    
    # Iterate over each security group
    for sg in security_groups:
        # Check if the security group has any inbound rules that allow unrestricted access (0.0.0.0/0)
        if any(rule['IpProtocol'] == '-1' and rule['IpRanges'] == ['0.0.0.0/0'] for rule in sg['IpPermissions']):
            print(f"Security group {sg['GroupId']} has an inbound rule that allows unrestricted access")
            
    # Get a list of all network ACLs in the current region
    acls = ec2.describe_network_acls()['NetworkAcls']
    
    # Iterate over each network ACL
    for acl in acls:
        # Check if the network ACL has any inbound rules that allow unrestricted access (0.0.0.0/0)
        if any(rule['RuleAction'] == 'allow' and rule['CidrBlock'] == '0.0.0.0/0' for rule in acl['Entries']):
            print(f"Network ACL {acl['NetworkAclId']} has an inbound rule that allows unrestricted access")
