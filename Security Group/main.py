import boto3
from tabulate import tabulate

ec2 = boto3.client('ec2')

response = ec2.describe_security_groups(
    GroupIds=['sg-025028548d0e7a3d0'],  # replace with your security group ID
)

for group in response['SecurityGroups']:
    print(f"Security Group Name: {group['GroupName']}")
    print(f"Security Group ID: {group['GroupId']}")

    print("Inbound rules:")
    inbound_table = [['Protocol', 'From Port', 'To Port', 'CIDR']]
    for rule in group['IpPermissions']:
        for ip_range in rule['IpRanges']:
            inbound_table.append([rule['IpProtocol'], rule.get('FromPort', 'N/A'), rule.get('ToPort', 'N/A'), ip_range['CidrIp']])
    print(tabulate(inbound_table, headers='firstrow'))

    print("Outbound rules:")
    outbound_table = [['Protocol', 'From Port', 'To Port', 'CIDR']]
    for rule in group['IpPermissionsEgress']:
        for ip_range in rule['IpRanges']:
            outbound_table.append([rule['IpProtocol'], rule.get('FromPort', 'N/A'), rule.get('ToPort', 'N/A'), ip_range['CidrIp']])
    print(tabulate(outbound_table, headers='firstrow'))