import boto3

# Initialize the S3 client
s3 = boto3.client('s3')
bucket_name = 'aws-163544304364-my-drive'

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

    print("All objects have been transitioned to Glacier storage class.")
else:
    print("No objects found in the bucket.")