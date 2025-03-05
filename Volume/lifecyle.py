import boto3
from datetime import datetime

def create_volume_lifecycle_policy():
    # Create DLM client
    dlm = boto3.client('dlm')
    ec2 = boto3.client('ec2')
    
    try:
        # Create lifecycle policy
        response = dlm.create_lifecycle_policy(
            ExecutionRoleArn='arn:aws:iam::0123456789:role/service-role/AWSDataLifecycleManagerDefaultRole',
            Description='30-day backup policy for volumes',
            State='ENABLED',
            PolicyDetails={
                'ResourceTypes': ['VOLUME'],
                'TargetTags': [{
                    'Key': 'Name',
                    'Value': 'Root'
                }],
                'Schedules': [{
                    'Name': '30-Day Snapshots',
                    'TagsToAdd': [{
                        'Key': 'Name',
                        'Value': f'Root {datetime.now().strftime("%B")}'  # Will show as "Root March"
                    }],
                    'CreateRule': {
                        'Interval': 24,
                        'IntervalUnit': 'HOURS',
                        'Times': ['09:00']
                    },
                    'RetainRule': {
                        'Count': 30
                    },
                    'CopyTags': True
                }]
            }
        )
        print("Successfully created lifecycle policy:", response['PolicyId'])
        
        # Tag the volumes with Name and Encrypted tags
        volumes = {
            'vol-0710d89881497064b': 'Root',
            'vol-043f197c5897da2ea': 'Webull Document'
        }
        
        for volume_id, name in volumes.items():
            ec2.create_tags(
                Resources=[volume_id],
                Tags=[
                    {'Key': 'Name', 'Value': name},
                    {'Key': 'Encrypted', 'Value': 'true'}
                ]
            )
            print(f"Tagged volume {volume_id} with Name: {name} and Encrypted: true")
            
    except Exception as e:
        print(f"Error creating lifecycle policy: {str(e)}")

if __name__ == "__main__":
    create_volume_lifecycle_policy()
