import boto3

def empty_bucket(bucket_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.objects.all().delete()

empty_bucket('aws-163544304364-backup')  # replace with your bucket name