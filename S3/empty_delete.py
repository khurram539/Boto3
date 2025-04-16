import boto3
from botocore.exceptions import ClientError

def empty_and_delete_bucket(bucket_name):
    """Empty and delete an S3 bucket."""
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    try:
        # Empty the bucket
        print(f"Emptying bucket: {bucket_name}")
        bucket.objects.all().delete()
        bucket.object_versions.all().delete()  # Delete versioned objects if versioning is enabled

        # Delete the bucket
        print(f"Deleting bucket: {bucket_name}")
        bucket.delete()
        print(f"Bucket {bucket_name} deleted successfully.")
    except ClientError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    bucket_name = "kaython-cloudtrail"  # Hardcoded bucket name
    empty_and_delete_bucket(bucket_name)