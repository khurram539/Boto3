import boto3
ec2 = boto3.resource('ec2')
instance_id = 'i-1234567890abcdef0' # replace with your instance ID
response = ec2.terminate_instances(InstanceIds=[instance_id])
print(response)
