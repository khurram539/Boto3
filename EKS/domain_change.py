import argparse
import sys

import boto3
from botocore.exceptions import BotoCoreError, ClientError


# Map private DNS names to desired EC2 Name tag values.
INSTANCES_TO_RENAME = {
    "ip-172-31-125-251.ec2.internal": "Worker-Node-1",
    "ip-172-31-160-161.ec2.internal": "Worker-Node-2",
    # "ip-172-31-127-131.ec2.internal": "Worker-Node-3",
}


def get_current_name_tag(instance: dict) -> str:
    tags = instance.get("Tags", [])
    for tag in tags:
        if tag.get("Key") == "Name":
            return tag.get("Value", "")
    return ""


def find_instance_by_private_dns(ec2_client, private_dns_name: str):
    response = ec2_client.describe_instances(
        Filters=[
            {"Name": "private-dns-name", "Values": [private_dns_name]},
            {"Name": "instance-state-name", "Values": ["pending", "running", "stopping", "stopped"]},
        ]
    )

    instances = []
    for reservation in response.get("Reservations", []):
        instances.extend(reservation.get("Instances", []))
    return instances


def rename_instances(region: str, apply_changes: bool) -> int:
    session = boto3.Session(region_name=region)
    ec2_client = session.client("ec2")

    print(f"Region: {region}")
    print("Mode: APPLY" if apply_changes else "Mode: DRY-RUN (no changes will be made)")

    failures = 0
    for private_dns_name, new_name in INSTANCES_TO_RENAME.items():
        print(f"\nLooking up: {private_dns_name}")
        try:
            instances = find_instance_by_private_dns(ec2_client, private_dns_name)
        except (BotoCoreError, ClientError) as err:
            failures += 1
            print(f"ERROR: Failed to describe instances for {private_dns_name}: {err}")
            continue

        if not instances:
            failures += 1
            print(f"WARN: No instances found for {private_dns_name}")
            continue

        if len(instances) > 1:
            print(f"WARN: Multiple instances found for {private_dns_name}; updating all matches")

        for instance in instances:
            instance_id = instance["InstanceId"]
            current_name = get_current_name_tag(instance)
            print(
                f"Instance: {instance_id} | Current Name: {current_name or '<none>'} | Target Name: {new_name}"
            )

            if current_name == new_name:
                print("SKIP: Name tag already matches target")
                continue

            if not apply_changes:
                print("DRY-RUN: Would update Name tag")
                continue

            try:
                ec2_client.create_tags(
                    Resources=[instance_id],
                    Tags=[{"Key": "Name", "Value": new_name}],
                )
                print("OK: Updated Name tag")
            except (BotoCoreError, ClientError) as err:
                failures += 1
                print(f"ERROR: Failed to update {instance_id}: {err}")

    return failures


def parse_args():
    parser = argparse.ArgumentParser(
        description="Rename EC2 Name tags using private DNS name mapping."
    )
    parser.add_argument(
        "--region",
        default="us-east-1",
        help="AWS region (default: us-east-1)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes (without this flag, script runs in dry-run mode)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    failures = rename_instances(region=args.region, apply_changes=args.apply)
    if failures:
        print(f"\nCompleted with {failures} issue(s)")
        return 1
    print("\nCompleted successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())