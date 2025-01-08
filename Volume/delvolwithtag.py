import boto3
from datetime import datetime

# Initialize a session using Amazon EC2
ec2 = boto3.client('ec2')

# Get the current month name
current_month = datetime.now().strftime('%B')

# Define the tag key and value
tag_key = 'Name'
tag_value = f'{current_month} Test'

# Find the volume with the specified tag
response = ec2.describe_volumes(
    Filters=[
        {
            'Name': f'tag:{tag_key}',
            'Values': [tag_value]
        }
    ]
)

volumes = response['Volumes']

if not volumes:
    print(f'No volumes found with tag {tag_key}: {tag_value}')
else:
    for volume in volumes:
        volume_id = volume['VolumeId']
        print(f'Found volume {volume_id} with tag {tag_key}: {tag_value}')
        
        # Confirm deletion
        confirm = input(f'Do you want to delete volume {volume_id}? (yes/no): ')
        if confirm.lower() == 'yes':
            ec2.delete_volume(VolumeId=volume_id)
            print(f'Volume {volume_id} deleted.')
        else:
            print(f'Volume {volume_id} not deleted.')
