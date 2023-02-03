import boto3

def scan_for_wasted_resources(event, context):
    # Create an AWS EC2 client
    ec2 = boto3.client('ec2')

    # Call the describe_instances method to retrieve a list of all EC2 instances
    instances = ec2.describe_instances()

    # Loop through each instance and check if it is underutilized
    for instance in instances['Reservations']:
        instance_id = instance['Instances'][0]['InstanceId']
        instance_type = instance['Instances'][0]['InstanceType']

        # Check if the instance is underutilized
        if is_underutilized(instance_id, instance_type):
            print("Instance %s is underutilized" % instance_id)

def is_underutilized(instance_id, instance_type):
    # TODO: Implement logic to check if an instance is underutilized
    return True
