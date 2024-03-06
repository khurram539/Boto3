import boto3

def get_last_attachment_date(volume_id):
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_volumes(VolumeIds=[volume_id])

    attachments = response['Volumes'][0]['Attachments']
    if attachments:
        last_attachment_time = max(attachment['AttachTime'] for attachment in attachments)
        return last_attachment_time
    else:
        return None

def list_volumes():
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_volumes(
        Filters=[
            {
                'Name': 'status',
                'Values': ['available']
            }
        ]
    )

    volumes = response['Volumes']
    volumes.sort(key=lambda x: x['CreateTime'])  # Sort volumes by creation time

    for volume in volumes:
        volume_id = volume['VolumeId']
        creation_time = volume['CreateTime'].strftime('%Y-%m-%d %H:%M:%S %Z')
        last_attachment_date = get_last_attachment_date(volume_id)
        
        if last_attachment_date:
            last_attachment_date_str = last_attachment_date.strftime('%Y-%m-%d %H:%M:%S %Z')
        else:
            last_attachment_date_str = 'Not attached'

        print("Volume ID: {}, Creation Time: {}, Last Attachment Date: {}".format(volume_id, creation_time, last_attachment_date_str))

if __name__ == "__main__":
    list_volumes()
