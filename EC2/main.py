import boto3
from tabulate import tabulate

# Create an EC2 client
ec2 = boto3.client('ec2')

# Retrieve information about instances
response = ec2.describe_instances()

# Initialize a list to hold instance information
instances_info = []

# Extract the required information from the response
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_id = instance['InstanceId']
        instance_type = instance['InstanceType']
        instance_state = instance['State']['Name']
        vpc_id = instance.get('VpcId', 'N/A')  # Use .get() for safer access
        subnet_id = instance.get('SubnetId', 'N/A')  # Use .get() for safer access
        public_ip = instance.get('PublicIpAddress', 'N/A')
        private_ip = instance.get('PrivateIpAddress', 'N/A')
        ami_id = instance['ImageId']  # Get the AMI ID
        
        # Append the extracted information to the instances_info list
        instances_info.append([instance_id, instance_type, instance_state, vpc_id, subnet_id, public_ip, private_ip, ami_id])

# Define headers for the table
headers = ["Instance ID", "Type", "State", "VPC ID", "Subnet ID", "Public IP", "Private IP", "AMI ID"]

# Use tabulate to print the table
print(tabulate(instances_info, headers=headers, tablefmt="grid"))