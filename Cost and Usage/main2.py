import boto3

# Create a Cost Explorer client
ce = boto3.client('ce', region_name='us-east-1')

# Set the time period for the query
time_period = {
    'Start': '2023-10-01',
    'End': '2023-10-30'
}

# Set the granularity of the query to MONTHLY
granularity = 'MONTHLY'

# Set the metrics to retrieve
metrics = ['UnblendedCost']

# Set the group by parameter to group by service
group_by = [
    {
        'Type': 'DIMENSION',
        'Key': 'SERVICE'
    }
]

# Call the get_cost_and_usage() method to get the data
response = ce.get_cost_and_usage(
    TimePeriod=time_period,
    Granularity=granularity,
    Metrics=metrics,
    GroupBy=group_by
)

# Print the results
for result in response['ResultsByTime']:
    for group in result['Groups']:
        print(f"Service: {group['Keys'][0]}")
        print(f"Unblended cost: {group['Metrics']['UnblendedCost']['Amount']} {group['Metrics']['UnblendedCost']['Unit']}")