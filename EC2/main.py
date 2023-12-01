import boto3

# Create an EC2 client using the default credential provider chain
ec2_client = boto3.client('ec2')

# Retrieve all EC2 instances
response = ec2_client.describe_instances()

# Iterate over the reservations and instances
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_id = instance['InstanceId']
        instance_type = instance['InstanceType']
        state = instance['State']['Name']
        
        print(f"Instance ID: {instance_id}")
        print(f"Instance Type: {instance_type}")
        print(f"State: {state}")
        print("------")
