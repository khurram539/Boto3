import boto3

# Initialize a session using Boto3
session = boto3.Session(region_name='us-east-1')

# Initialize the EC2 client
ec2_client = session.client('ec2')

# Define the private DNS names and their new names
instances_to_rename = {
    'ip-192-168-8-100.ec2.internal': 'Worker-Node-1',
    'ip-192-168-58-189.ec2.internal': 'Worker-Node-2',
    'ip-192-168-89-131.ec2.internal': 'Worker-Node-3'
}

# Iterate over each private DNS name and update the Name tag
for private_dns_name, new_name in instances_to_rename.items():
    # Retrieve the instance ID using the private DNS name
    response = ec2_client.describe_instances(
        Filters=[
            {'Name': 'private-dns-name', 'Values': [private_dns_name]}
        ]
    )

    # Check if any instances were found
    if not response['Reservations']:
        print(f"No instances found with private DNS name: {private_dns_name}")
    else:
        instance_id = response['Reservations'][0]['Instances'][0]['InstanceId']
        print(f"Found instance ID: {instance_id} for private DNS name: {private_dns_name}")

        # Update the Name tag for the instance
        ec2_client.create_tags(
            Resources=[instance_id],
            Tags=[
                {'Key': 'Name', 'Value': new_name}
            ]
        )
        print(f"Updated instance {instance_id} name to {new_name}")