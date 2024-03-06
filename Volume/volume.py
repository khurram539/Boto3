import boto3
from datetime import datetime, timezone

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
    response = ec2_client.describe_volumes()

    volumes = response['Volumes']
    for volume in volumes:
        volume_id = volume['VolumeId']
        last_attachment_date = get_last_attachment_date(volume_id)
        
        if last_attachment_date:
            last_attachment_date_str = last_attachment_date.strftime('%Y-%m-%d %H:%M:%S %Z')
        else:
            last_attachment_date_str = 'Not attached'

        print(f"Volume ID: {volume_id}, Last Attachment Date: {last_attachment_date_str}")

if __name__ == "__main__":
    list_volumes()

