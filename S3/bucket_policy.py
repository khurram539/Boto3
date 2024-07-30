import boto3
import json

# Initialize the S3 client
s3 = boto3.client('s3')
bucket_name = 'aws-163544304364-my-drive'

# Retrieve the bucket policy of the specified bucket
try:
	result = s3.get_bucket_policy(Bucket=bucket_name)
	print("Current Bucket Policy:")
	print(result['Policy'])
except s3.exceptions.from_code('NoSuchBucketPolicy'):
	print("No existing bucket policy found.")
except s3.exceptions.NoSuchBucket:
	print("The specified bucket does not exist.")
except Exception as e:
	print(f"An error occurred: {e}")

# Define the bucket policy
policy = {
	"Version": "2012-10-17",
	"Id": "BucketPolicy",
	"Statement": [
		{
			"Sid": "AllowRootAndSpecificUser",
			"Effect": "Allow",
			"Principal": {
				"AWS": [
					"arn:aws:iam::163544304364:root",
					"arn:aws:iam::163544304364:user/k.khoja"
				]
			},
			"Action": "s3:*",
			"Resource": [
				f"arn:aws:s3:::{bucket_name}",
				f"arn:aws:s3:::{bucket_name}/*"
			]
		}
	]
}

# Convert the policy to a JSON string
policy_json = json.dumps(policy)

# Apply the new bucket policy
s3.put_bucket_policy(Bucket=bucket_name, Policy=policy_json)
print("New bucket policy applied successfully.")