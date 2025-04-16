import boto3
import subprocess
from botocore.exceptions import ClientError

def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None or region == 'us-east-1':
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        print(e)
        return False
    return True

# Example usage
if __name__ == "__main__":
    bucket_name = 'kaytheon-cloudtrail'
    region = 'us-east-1'  # Specify your region
    if create_bucket(bucket_name, region):
        print(f'Bucket {bucket_name} created successfully.')
    else:
        print(f'Failed to create bucket {bucket_name}.')

# To list all the AWS S3 buckets

subprocess.run(["aws", "s3", "ls"])

