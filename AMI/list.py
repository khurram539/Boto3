import boto3
from datetime import datetime

def list_amis():
    # Create an EC2 resource
    ec2 = boto3.resource('ec2')

    # List all AMIs
    images = ec2.images.filter(Owners=['self'])  # Use 'self' to list AMIs owned by you; remove filter to list all available AMIs

    # Fetch AMIs with their creation dates
    amis = [(image.name, image.id, image.creation_date.split('T')[0], image.state) for image in images]

    # Sort AMIs by creation date in descending order
    sorted_amis = sorted(amis, key=lambda x: x[2], reverse=True)

    for ami in sorted_amis:
        print(f"Name: {ami[0]}, ID: {ami[1]}, Creation Date: {ami[2]}, Status: {ami[3]}")

if __name__ == "__main__":
    list_amis()