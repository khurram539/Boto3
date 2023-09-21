import boto3



#client = boto3.client('s3')

s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
    print(bucket.name)








#response = client.list_buckets()

#this is a test



