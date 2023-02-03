import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    # Get the list of instances
    instances = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': ['MyWindowsServer']
            }
        ]
    )

    # Loop through the instances
    for instance in instances['Reservations']:
        instance_id = instance['Instances'][0]['InstanceId']

        # Create a snapshot of the instance's root volume
        snapshot = ec2.create_snapshot(
            VolumeId=instance['Instances'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeId'],
            Description='Snapshot of MyWindowsServer'
        )

        # Tag the snapshot with the same Name tag as the instance
        ec2.create_tags(
            Resources=[snapshot['SnapshotId']],
            Tags=[{
                'Key': 'Name',
                'Value': 'MyWindowsServer-backup'
            }]
        )
