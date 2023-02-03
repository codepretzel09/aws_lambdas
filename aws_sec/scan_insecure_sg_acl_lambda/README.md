This lambda function uses the boto3 library to access the EC2 service, and it scans all security groups and network ACLs in the current region for rules that allow unrestricted access (0.0.0.0/0). If such a rule is found, it prints a message to indicate which security group or network ACL has the insecure rule.

You can customize this lambda function to perform additional actions, such as sending an alert or automatically updating the security group or network ACL to remove the insecure rule.
