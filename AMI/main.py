import boto3
import logging
from botocore.exceptions import ClientError
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Create EC2 client
ec2_client = boto3.client('ec2')

# Get the current date in the format mm/dd/yyyy
current_date = datetime.now().strftime("%m/%d/%Y")

# Function to create an AMI from an instance
def create_ami(instance_id, ami_name):
    try:
        response = ec2_client.create_image(
            InstanceId=instance_id,
            Name=ami_name,
            NoReboot=True  # Optional: ensures the instance is not rebooted
        )
        ami_id = response['ImageId']
        logger.info(f'AMI creation initiated, ID: {ami_id}')
        tag_ami(ami_id, ami_name)  # Tag the AMI with the given name
        return ami_id
    except ClientError as e:
        logger.error(f'Error creating AMI: {e}')
        return None

# Function to tag the AMI with a name
def tag_ami(ami_id, ami_name):
    try:
        ec2_client.create_tags(
            Resources=[ami_id],
            Tags=[
                {
                    'Key': 'Name',
                    'Value': ami_name
                }
            ]
        )
        logger.info(f'AMI {ami_id} tagged with Name: {ami_name}')
    except ClientError as e:
        logger.error(f'Error tagging AMI: {e}')

# Function to wait for the AMI to become available
def wait_for_ami(ami_id):
    waiter = ec2_client.get_waiter('image_available')
    try:
        waiter.wait(ImageIds=[ami_id])
        logger.info(f'AMI {ami_id} is now available.')
    except ClientError as e:
        logger.error(f'Error waiting for AMI: {e}')

# Example usage
instance_id = 'i-05f55c2148eb7c5e3'
ami_name = f'(Ubuntu Desktop {current_date}'
ami_id = create_ami(instance_id, ami_name)

if ami_id:
    wait_for_ami(ami_id)

