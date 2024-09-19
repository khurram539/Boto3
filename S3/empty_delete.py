import boto3
from botocore.exceptions import ClientError

def empty_bucket(bucket_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    try:
        bucket.objects.all().delete()
        print(f"All objects in bucket '{bucket_name}' have been deleted.")
    except ClientError as e:
        print(f"Error deleting objects in bucket '{bucket_name}': {e}")

def delete_bucket(bucket_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    try:
        bucket.delete()
        print(f"Bucket '{bucket_name}' has been deleted.")
    except ClientError as e:
        print(f"Error deleting bucket '{bucket_name}': {e}")

def empty_and_delete_bucket(bucket_name):
    empty_bucket(bucket_name)
    delete_bucket(bucket_name)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Empty and delete an S3 bucket.")
    parser.add_argument("bucket_name", help="The name of the S3 bucket to empty and delete.")
    args = parser.parse_args()

    empty_and_delete_bucket(args.bucket_name)
    print(f"Your bucket '{args.bucket_name}' has been emptied and deleted successfully.")
    
# Enter the follow commands to run the script:
# python3 empty.py aws-163544304364-billing