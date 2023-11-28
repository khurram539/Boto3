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



In this code, we use the `lookup_events()` method of the CloudTrail client to search for events with the event name `'CreateBucket'`. The response will contain a list of events, and we iterate over each event to retrieve the bucket name and user identity from the event data.

Please note that you need to have the necessary permissions to access CloudTrail and S3, and CloudTrail must be enabled and configured to capture the necessary events for this information to be available.
