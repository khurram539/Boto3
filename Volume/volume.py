import boto3

ec2  = boto3.resource('ec2')

# Filter to only include volumes that are available
filters = [{
    'Name': 'status',
    'Values': ['available']
}]

volumes = ec2.volumes.filter(Filters=filters)

# Create a list of tuples containing volume id and detach time
volume_list = []
for volume in volumes:
    if volume.attachments:
        detach_time = volume.attachments[0]['DetachTime'] if 'DetachTime' in volume.attachments[0] else None
        volume_list.append((volume.id, detach_time))
    else:
        volume_list.append((volume.id, None))

# Sort the list by detach time
#volume_list.sort(key=lambda x: x[1])

for volume_id, detach_time in volume_list:
    print(volume_id, detach_time if detach_time else 'Never detached')
