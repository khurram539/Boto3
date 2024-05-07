import boto3
from tabulate import tabulate
from datetime import datetime

# Create an IAM client
iam = boto3.client('iam')

# Get a list of all IAM users
users = iam.list_users()['Users']

# Iterate through the users and get their details
data = []
for user in users:
    username = user['UserName']
    
    # Get the user's group memberships
    groups = iam.list_groups_for_user(UserName=username)['Groups']
    group_names = [group['GroupName'] for group in groups]
    
    # Get the user's last activity
    try:
        last_login = iam.get_user(UserName=username)['User']['PasswordLastUsed']
        last_activity = last_login.strftime('%Y-%m-%d %H:%M:%S')
    except (KeyError, AttributeError):
        last_activity = 'N/A'
    
    # Get the user's console last sign-in
    try:
        last_console_sign_in = iam.get_user(UserName=username)['User']['ConsoleLastAccess']
        last_console_sign_in = last_console_sign_in.strftime('%Y-%m-%d %H:%M:%S')
    except (KeyError, AttributeError):
        last_console_sign_in = 'N/A'
    
    # Get the user's MFA status
    mfa_devices = iam.list_mfa_devices(UserName=username)['MFADevices']
    mfa_status = 'Enabled' if mfa_devices else 'Disabled'
    
    data.append([username, ', '.join(group_names), last_activity, last_console_sign_in, mfa_status])

# Print the results in a table
print(tabulate(data, headers=['IAM User', 'Groups', 'Last Activity', 'Console Last Sign-in', 'MFA Status'], tablefmt='grid'))


