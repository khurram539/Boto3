import boto3

# Initialize the S3 client
s3 = boto3.client('s3')

# List of S3 bucket names
bucket_names = [
    'aws-163544304364-my-drive',
    'aws-163544304364-repo',
    'aws-163544304364-keys',
    'aws-163544304364-billing',
    'aws-163544304364-devbox'
    # Add more bucket names as needed
]

# Iterate over each bucket
for bucket_name in bucket_names:
    print(f"Processing bucket: {bucket_name}")
    
    # List all objects in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)

    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            
            # Copy the object to the same location with the storage class set to Glacier
            s3.copy_object(
                Bucket=bucket_name,
                CopySource={'Bucket': bucket_name, 'Key': key},
                Key=key,
                StorageClass='GLACIER_IR' # Glacier Infrequent Access storage class
            )
            
            # Optionally, delete the original object if needed
            # s3.delete_object(Bucket=bucket_name, Key=key)

        print(f"All objects in bucket {bucket_name} have been transitioned to Glacier storage class.")
    else:
        print(f"No objects found in bucket {bucket_name}.")