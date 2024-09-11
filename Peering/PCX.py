import boto3

# Initialize a session using Boto3
session = boto3.Session(region_name='us-east-1')

# Initialize the EC2 client
ec2_client = session.client('ec2')

# Define VPC IDs and CIDR blocks
vpc_id_1 = 'vpc-0f238901bc3467b62'
vpc_id_2 = 'vpc-0ecb6b3385c3e095e'
cidr_block_1 = '172.31.0.0/16'
cidr_block_2 = '192.168.0.0/16'

# Create VPC peering connection
peering_connection = ec2_client.create_vpc_peering_connection(
    VpcId=vpc_id_1,
    PeerVpcId=vpc_id_2
)

peering_connection_id = peering_connection['VpcPeeringConnection']['VpcPeeringConnectionId']
print(f'Created VPC peering connection: {peering_connection_id}')

# Accept VPC peering connection
ec2_client.accept_vpc_peering_connection(
    VpcPeeringConnectionId=peering_connection_id
)
print(f'Accepted VPC peering connection: {peering_connection_id}')

# Get route tables for both VPCs
route_tables_1 = ec2_client.describe_route_tables(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id_1]}])
route_tables_2 = ec2_client.describe_route_tables(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id_2]}])

# Update route tables to allow traffic between VPCs
for route_table in route_tables_1['RouteTables']:
    ec2_client.create_route(
        RouteTableId=route_table['RouteTableId'],
        DestinationCidrBlock=cidr_block_2,
        VpcPeeringConnectionId=peering_connection_id
    )
    print(f'Updated route table {route_table["RouteTableId"]} in VPC {vpc_id_1}')

for route_table in route_tables_2['RouteTables']:
    ec2_client.create_route(
        RouteTableId=route_table['RouteTableId'],
        DestinationCidrBlock=cidr_block_1,
        VpcPeeringConnectionId=peering_connection_id
    )
    print(f'Updated route table {route_table["RouteTableId"]} in VPC {vpc_id_2}')

# Update security groups to allow traffic between VPCs
security_groups_1 = ec2_client.describe_security_groups(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id_1]}])
security_groups_2 = ec2_client.describe_security_groups(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id_2]}])

for sg in security_groups_1['SecurityGroups']:
    ec2_client.authorize_security_group_ingress(
        GroupId=sg['GroupId'],
        IpPermissions=[
            {
                'IpProtocol': '-1',
                'IpRanges': [{'CidrIp': cidr_block_2}]
            }
        ]
    )
    print(f'Updated security group {sg["GroupId"]} in VPC {vpc_id_1}')

for sg in security_groups_2['SecurityGroups']:
    ec2_client.authorize_security_group_ingress(
        GroupId=sg['GroupId'],
        IpPermissions=[
            {
                'IpProtocol': '-1',
                'IpRanges': [{'CidrIp': cidr_block_1}]
            }
        ]
    )
    print(f'Updated security group {sg["GroupId"]} in VPC {vpc_id_2}')