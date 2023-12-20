from tabulate import tabulate
import boto3

# Create a Cost Explorer client
ce = boto3.client('ce', region_name='us-east-1')

# Set the time period for the query
time_period = {
    'Start': '2023-12-01',
    'End': '2023-12-31'
}

# Set the granularity of the query to MONTHLY
granularity = 'MONTHLY'

# Set the metrics to retrieve
metrics = ['BlendedCost']

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

# Create a list to store the results
costs = []

# Add the results to the list
for result in response['ResultsByTime']:
    for group in result['Groups']:
        costs.append([group['Keys'][0], group['Metrics']['BlendedCost']['Amount']])

# Tabulate the results
print(tabulate(costs, headers=['Service', 'Cost'], tablefmt='pretty'))