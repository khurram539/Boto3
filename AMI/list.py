from datetime import datetime
import boto3
from tabulate import tabulate

def list_amis():
    ec2 = boto3.resource('ec2')

    images = ec2.images.filter(Owners=['self'])

    amis = [
        (
            image.name,
            image.id,
            image.creation_date.split('T')[0],
            image.state
        )
        for image in images
    ]

    # Sort by date (newest first)
    sorted_amis = sorted(amis, key=lambda x: x[2], reverse=True)

    # Define headers
    headers = ["Name", "AMI ID", "Creation Date", "State"]

    # Print table
    print(tabulate(sorted_amis, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    list_amis()
