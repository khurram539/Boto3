import boto3
from botocore.exceptions import ClientError

def terminate_eks_cluster(cluster_name):
    # Initialize a boto3 EKS client
    eks_client = boto3.client('eks')
    
    try:
        # Terminate the specified EKS cluster
        response = eks_client.delete_cluster(name=cluster_name)
        print(f"Cluster '{cluster_name}' is being terminated.")
        return response
    except ClientError as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
cluster_name = 'my-eks-cluster'
terminate_eks_cluster(cluster_name)
