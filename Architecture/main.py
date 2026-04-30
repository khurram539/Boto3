import boto3
import json

def get_vpcs(ec2):
    return ec2.describe_vpcs()['Vpcs']

def get_subnets(ec2):
    return ec2.describe_subnets()['Subnets']

def get_instances(ec2):
    reservations = ec2.describe_instances()['Reservations']
    instances = []
    for r in reservations:
        for i in r['Instances']:
            instances.append({
                'InstanceId': i['InstanceId'],
                'Type': i['InstanceType'],
                'State': i['State']['Name'],
                'SubnetId': i.get('SubnetId'),
                'PublicIp': i.get('PublicIpAddress')
            })
    return instances

def get_igw(ec2):
    return ec2.describe_internet_gateways()['InternetGateways']

def get_nat(ec2):
    return ec2.describe_nat_gateways()['NatGateways']

def get_rds():
    rds = boto3.client('rds')
    return rds.describe_db_instances()['DBInstances']

def get_s3():
    s3 = boto3.client('s3')
    return s3.list_buckets()['Buckets']

def get_elb():
    elb = boto3.client('elbv2')
    return elb.describe_load_balancers()['LoadBalancers']

def get_eks():
    eks = boto3.client('eks')
    clusters = eks.list_clusters()['clusters']
    details = []
    for c in clusters:
        details.append(eks.describe_cluster(name=c)['cluster'])
    return details

def main():
    session = boto3.Session()
    region = session.region_name or "us-east-1"

    ec2 = boto3.client('ec2', region_name=region)

    data = {
        "Region": region,
        "VPCs": get_vpcs(ec2),
        "Subnets": get_subnets(ec2),
        "EC2_Instances": get_instances(ec2),
        "InternetGateways": get_igw(ec2),
        "NATGateways": get_nat(ec2),
        "LoadBalancers": get_elb(),
        "RDS": get_rds(),
        "S3": get_s3(),
        "EKS": get_eks()
    }

    print(json.dumps(data, indent=2, default=str))

if __name__ == "__main__":
    main()