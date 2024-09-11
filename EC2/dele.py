import boto3

# Initialize a session using Amazon EC2
ec2 = boto3.client('ec2')

# Instance ID
instance_id = 'i-09a255516077bbd1e'

# Modify the instance attribute to allow termination
ec2.modify_instance_attribute(
    InstanceId=instance_id,
    DisableApiTermination={
        'Value': False
    }
)

# Terminate the instance
response = ec2.terminate_instances(InstanceIds=[instance_id])
print(response)
