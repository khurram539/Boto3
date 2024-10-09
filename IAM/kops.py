import boto3

# Initialize a session using Amazon IAM
iam = boto3.client('iam')

# Create a user
user_name = 'kops'
iam.create_user(UserName=user_name)

# List of policies to attach
policies = [
    'arn:aws:iam::aws:policy/AmazonEC2FullAccess',
    'arn:aws:iam::aws:policy/AmazonRoute53FullAccess',
    'arn:aws:iam::aws:policy/AmazonS3FullAccess',
    'arn:aws:iam::aws:policy/IAMFullAccess',
    'arn:aws:iam::aws:policy/AmazonVPCFullAccess',
    'arn:aws:iam::aws:policy/AmazonSQSFullAccess',
    'arn:aws:iam::aws:policy/AmazonEventBridgeFullAccess'
]

# Attach policies to the user
for policy_arn in policies:
    iam.attach_user_policy(UserName=user_name, PolicyArn=policy_arn)

print(f"User {user_name} created and policies attached.")