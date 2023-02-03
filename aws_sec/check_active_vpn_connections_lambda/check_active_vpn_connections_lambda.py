import boto3

def lambda_handler(event, context):
    # create an EC2 client
    ec2 = boto3.client('ec2')
    
    # get the current VPN endpoint connections
    vpn_connections = ec2.describe_vpn_connections()
    
    # loop through the VPN connections and print the connection details
    for connection in vpn_connections['VpnConnections']:
        print(f'VPN connection ID: {connection["VpnConnectionId"]}')
        print(f'VPN connection state: {connection["State"]}')
        print(f'VPN connection type: {connection["Type"]}')
        print(f'Customer gateway ID: {connection["CustomerGatewayId"]}')
        print(f'VPN gateway ID: {connection["VpnGatewayId"]}')
        print(f'VPN tunnel options: {connection["Options"]}')
        print('---')

