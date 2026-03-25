import boto3

ec2 = boto3.client('ec2', region_name='us-east-1')

# Create an EIP
allocation = ec2.allocate_address(Domain='vpc')

# Attach the EIP to your instance
response = ec2.associate_address(
    InstanceId='i-05a352937c930c9a5',  # replace with your instance ID
    AllocationId=allocation['AllocationId']
)

print(response)