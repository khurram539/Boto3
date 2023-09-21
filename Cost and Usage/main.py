import boto3

# Create a Cost Explorer client
ce = boto3.client('ce', region_name='us-east-1')

# Set the time period for the query
time_period = {
    'Start': '2023-01-01',
    'End': '2023-09-30'
}

# Set the granularity of the query to MONTHLY
granularity = 'MONTHLY'

# Set the metrics to retrieve
metrics = ['UnblendedCost']


# Call the get_cost_and_usage() method to get the data
response = ce.get_cost_and_usage(
    TimePeriod=time_period,
    Granularity=granularity,
    Metrics=metrics
)

# Print the results
for result in response['ResultsByTime']:
    print(f"Time period: {result['TimePeriod']['Start']} to {result['TimePeriod']['End']}")
    print(f"Unblended cost: {result['Total']['UnblendedCost']['Amount']} {result['Total']['UnblendedCost']['Unit']}")