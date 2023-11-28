import boto3

# Create a Boto3 client for CloudTrail
cloudtrail_client = boto3.client('cloudtrail')

# Specify the event name for bucket creation
event_name = 'CreateBucket'

# Search for the CreateBucket events
response = cloudtrail_client.lookup_events(
    LookupAttributes=[
        {
            'AttributeKey': 'EventName',
            'AttributeValue': event_name
        }
    ]
)

# Iterate over the events and retrieve the user identity
for event in response['Events']:
    bucket_name = event['Resources'][0]['ResourceName']
    user_identity = event['Username']
    print(f"The S3 bucket {bucket_name} was created by {user_identity}")
