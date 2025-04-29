import boto3
import logging
import time
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# AWS clients
ssm_client = boto3.client('ssm')
s3_client = boto3.client('s3')

# S3 bucket for storing logs
S3_BUCKET_NAME = 'kaytheon-system-manager'


def get_all_instance_ids():
    """Retrieve all managed instance IDs from AWS Systems Manager."""
    try:
        instance_ids = []
        paginator = ssm_client.get_paginator('describe_instance_information')
        for page in paginator.paginate():
            for instance in page['InstanceInformationList']:
                instance_ids.append(instance['InstanceId'])
        logger.info(f"Found instances: {instance_ids}")
        return instance_ids
    except ClientError as e:
        logger.error(f"Error retrieving instance IDs: {e}")
        return []


def run_patch_now(instance_ids):
    """Run patching on all instances."""
    try:
        response = ssm_client.send_command(
            InstanceIds=instance_ids,
            DocumentName='AWS-RunPatchBaseline',
            Parameters={
                'Operation': ['Install'],
                'RebootOption': ['NoReboot']  # Prevent automatic reboot
            },
            TimeoutSeconds=600  # Timeout for the command
        )
        logger.info(
            f"Patch command sent. Command ID: {
                response['Command']['CommandId']}")
        return response['Command']['CommandId']
    except ClientError as e:
        logger.error(f"Error running patch now: {e}")
        return None


def upload_logs_to_s3(command_id):
    """Retrieve patching logs and upload them to S3."""
    try:
        paginator = ssm_client.get_paginator('list_command_invocations')
        for page in paginator.paginate(CommandId=command_id, Details=True):
            for invocation in page['CommandInvocations']:
                instance_id = invocation['InstanceId']
                log_output = invocation.get('StandardOutputContent', '')
                if log_output:
                    file_name = f"{instance_id}_patch_log.txt"
                    s3_client.put_object(
                        Bucket=S3_BUCKET_NAME,
                        Key=file_name,
                        Body=log_output
                    )
                    logger.info(
                        f"Uploaded log for instance {instance_id} to S3: {file_name}")
    except ClientError as e:
        logger.error(f"Error uploading logs to S3: {e}")


def check_command_status(command_id):
    """Check the status of the patching command."""
    try:
        all_success = True
        while True:
            response = ssm_client.list_command_invocations(
                CommandId=command_id,
                Details=True
            )
            statuses = []
            for invocation in response['CommandInvocations']:
                instance_id = invocation['InstanceId']
                status = invocation['Status']
                statuses.append(status)
                logger.info(f"Instance {instance_id} patching status: {status}")
                if status == 'Failed':
                    logger.warning(f"Instance {instance_id} patching did not complete successfully.")
                    all_success = False

            # Check if all statuses are no longer "InProgress"
            if all(status != 'InProgress' for status in statuses):
                break

            logger.info("Patching still in progress. Waiting for 30 seconds...")
            time.sleep(30)

        if all_success:
            logger.info("All instances were successfully patched.")
        else:
            logger.warning("Some instances failed to patch.")
    except ClientError as e:
        logger.error(f"Error checking command status: {e}")


def main():
    # Step 1: Get all instance IDs
    instance_ids = get_all_instance_ids()
    if not instance_ids:
        logger.error("No instances found to patch.")
        return

    # Step 2: Run patch now
    command_id = run_patch_now(instance_ids)
    if not command_id:
        logger.error("Failed to send patch command.")
        return

    # Step 3: Upload logs to S3
    upload_logs_to_s3(command_id)

    # Step 4: Check patching status
    check_command_status(command_id)


if __name__ == "__main__":
    main()

# pip install autopep8
# autopep8 --in-place --aggressive --aggressive PatchNow.py
