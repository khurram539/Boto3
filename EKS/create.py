import boto3
import json
from botocore.exceptions import ClientError

def create_iam_role(role_name, assume_role_policy_document):
    """Create an IAM role with the specified name and policy document."""
    iam_client = boto3.client('iam')
    try:
        response = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(assume_role_policy_document)
        )
        print(f"Role created: {response['Role']['Arn']}")
        return response['Role']['Arn']
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print(f"Role {role_name} already exists.")
            response = iam_client.get_role(RoleName=role_name)
            return response['Role']['Arn']
        else:
            print(e)
            return None

def attach_policies_to_role(role_name, policies):
    """Attach the specified policies to the IAM role."""
    iam_client = boto3.client('iam')
    for policy_arn in policies:
        try:
            iam_client.attach_role_policy(
                RoleName=role_name,
                PolicyArn=policy_arn
            )
            print(f"Attached policy {policy_arn} to role {role_name}")
        except ClientError as e:
            print(e)

def create_eks_cluster(cluster_name, role_arn, subnet_ids, security_group_ids):
    """Create an EKS cluster with the specified parameters."""
    eks_client = boto3.client('eks')
    try:
        response = eks_client.create_cluster(
            name=cluster_name,
            version='1.30',  # Specify the EKS version
            roleArn=role_arn,
            resourcesVpcConfig={
                'subnetIds': subnet_ids,
                'securityGroupIds': security_group_ids
            }
        )
        print(f"Cluster creation initiated: {response['cluster']['status']}")
    except ClientError as e:
        print(e)

# Example usage
if __name__ == "__main__":
    cluster_name = 'my-eks-cluster'
    role_name = 'EKSClusterRole'
    region = 'us-east-1'
    subnet_ids = ['subnet-08d90b90e9b121c7e', 'subnet-01d84fc63df0a696c']  # Replace with your subnet IDs
    security_group_ids = ['sg-025028548d0e7a3d0']  # Replace with your security group IDs
    
    # Trust policy document
    assume_role_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "eks.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    policies = [
        'arn:aws:iam::aws:policy/AmazonEKSClusterPolicy',
        'arn:aws:iam::aws:policy/AmazonEKSServicePolicy'
    ]
    
    # Create IAM role or get existing role ARN
    role_arn = create_iam_role(role_name, assume_role_policy_document)
    
    if role_arn:
        # Attach policies to the role
        attach_policies_to_role(role_name, policies)
        
        # Create the EKS cluster
        create_eks_cluster(cluster_name, role_arn, subnet_ids, security_group_ids)