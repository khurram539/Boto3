import boto3
from botocore.exceptions import ClientError

def delete_s3_bucket(bucket_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    
    try:
        # Delete all objects in the bucket
        bucket.objects.all().delete()
        
        # Check if versioning is enabled and delete all versions
        if bucket.versioning.status == 'Enabled':
            bucket.object_versions.all().delete()
        
        # Delete the bucket
        bucket.delete()
        print(f"Bucket '{bucket_name}' was deleted successfully.")
    except ClientError as e:
        print(f"Failed to delete bucket '{bucket_name}': {e}")

# Replace 'your-bucket-name' with the name of your bucket
delete_s3_bucket('aws-163544304364-scripts')