# Look up all EC2 instances, instance names, and instance types          
import boto3

# Create an EC2 client
ec2 = boto3.client('ec2')

# Call describe_instances(), which returns a dictionary
response = ec2.describe_instances()

# Loop through the Reservations list in the dictionary
for reservation in response["Reservations"]:
    # Loop through the Instances list in the dictionary
    for instance in reservation["Instances"]:
        # Initialize variables for instance name and type
        instance_name = ""
        instance_type = ""
        # Loop through the Tags list in the dictionary
        for tag in instance["Tags"]:
            # Check if the tag key is "Name"
            if tag["Key"] == "Name":
                # Set the instance name
                instance_name = tag["Value"]
        # Set the instance type
        instance_type = instance["InstanceType"]
        # Print the instance ID, name, and type
        print(f"Instance ID: {instance['InstanceId']}, Name: {instance_name}, Type: {instance_type}")