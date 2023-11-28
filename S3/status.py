import boto3

# Create a Boto3 client for S3
client = boto3.client('s3')

# List all S3 buckets
response = client.list_buckets()

# Iterate over each bucket and check if it is encrypted
for bucket in response['Buckets']:
    bucket_name = bucket['Name']
    bucket_encryption = client.get_bucket_encryption(Bucket=bucket_name)
    if 'ServerSideEncryptionConfiguration' in bucket_encryption:
        print(f"Bucket {bucket_name} is encrypted")
    else:
        print(f"Bucket {bucket_name} is not encrypted")
