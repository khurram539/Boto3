import boto3

# Create an EC2 client
ec2 = boto3.client('ec2')

# Retrieve information about instances
response = ec2.describe_instances()

# Extract the required information from the response
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_id = instance['InstanceId']
        instance_type = instance['InstanceType']
        instance_state = instance['State']['Name']
        vpc_id = instance['VpcId']
        subnet_id = instance['SubnetId']
        public_ip = instance.get('PublicIpAddress', 'N/A')
        private_ip = instance.get('PrivateIpAddress', 'N/A')
        
        # Print the instance details
        print(f"Instance ID: {instance_id}")
        print(f"Instance Type: {instance_type}")
        print(f"Instance State: {instance_state}")
        print(f"VPC ID: {vpc_id}")
        print(f"Subnet ID: {subnet_id}")
        print(f"Public IP: {public_ip}")
        print(f"Private IP: {private_ip}")
        print()
