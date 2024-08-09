# import boto3
# ec2 = boto3.resource('ec2')
# instance_id = 'i-0ce11afb16ba5ebd8' # replace with your instance ID
# response = ec2.terminate_instances(InstanceIds=[instance_id])
# print(response)


import boto3
ec2 = boto3.resource('ec2')
instance_id = 'i-0f605656dbd24ffa8'
response = ec2.instances.filter(InstanceIds=[instance_id]).terminate()
print(response)
