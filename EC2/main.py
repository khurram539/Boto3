import boto3

# Create an EC2 client
ec2 = boto3.client('ec2')

# Retrieve information about instances
response = ec2.describe_instances()

# Extract the required information from the response
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_id = instance['InstanceId']
        instance_type = instance['InstanceType']
        instance_state = instance['State']['Name']
        vpc_id = instance['VpcId']
        subnet_id = instance['SubnetId']
        public_ip = instance.get('PublicIpAddress', 'N/A')
        private_ip = instance.get('PrivateIpAddress', 'N/A')
        ami_id = instance['ImageId']  # Get the AMI ID
        
        # Get the details of the AMI
        ami_response = ec2.describe_images(ImageIds=[ami_id])
        ami_name = ami_response['Images'][0]['Name']  
        
         # Get the platform details
        platform_details = instance.get('Platform', 'N/A')  # Get the platform details
        
        # Determine the operating system based on the platform details and the AMI name
        if platform_details == 'windows':
            operating_system = 'Windows'
        elif 'linux' in ami_name.lower():
            operating_system = 'Linux'
        else:
            operating_system = 'Unknown'
        
        # Print the instance details        
        print(f"Instance name: {instance['Tags'][0]['Value']}")
        print(f"Availability Zone: {instance['Placement']['AvailabilityZone']}")
        print(f"Instance State: {instance_state}")
        print(f"Instance Type: {instance_type}")
        print(f"Instance ID: {instance_id}") 
        print(f"VPC ID: {vpc_id}")        
        print(f"Subnet ID: {subnet_id}")        
        print(f"Public IP: {public_ip}")        
        print(f"Private IP: {private_ip}")
        print(f"AMI Name:  {ami_name}")        
        print(f"AMI ID: {ami_id}")
        print("-------------------------------")
             
        
        
        
        
         
        
        
        
        
        
