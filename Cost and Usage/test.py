from tabulate import tabulate
import boto3
from datetime import datetime, timedelta
import csv

# Create Cost Explorer client
ce = boto3.client('ce', region_name='us-east-1')

# Dynamic time range (last 12 months)
end = datetime.today()
start = end - timedelta(days=365)

time_period = {
    'Start': start.strftime('%Y-%m-%d'),
    'End': end.strftime('%Y-%m-%d')
}

# Request parameters
params = {
    'TimePeriod': time_period,
    'Granularity': 'MONTHLY',
    'Metrics': ['UnblendedCost'],
    'GroupBy': [
        {
            'Type': 'DIMENSION',
            'Key': 'SERVICE'
        }
    ]
}

# Store aggregated results
service_totals = {}

# Handle pagination
while True:
    response = ce.get_cost_and_usage(**params)

    for result in response['ResultsByTime']:
        for group in result['Groups']:
            service = group['Keys'][0]
            amount = float(group['Metrics']['UnblendedCost']['Amount'])

            if service not in service_totals:
                service_totals[service] = 0.0

            service_totals[service] += amount

    # Check for next page
    if 'NextPageToken' in response:
        params['NextPageToken'] = response['NextPageToken']
    else:
        break

# Convert to table format
costs = [[service, round(cost, 2)] for service, cost in service_totals.items()]

# Sort by highest cost
costs.sort(key=lambda x: x[1], reverse=True)

# Calculate total
total_cost = sum(service_totals.values())

# Print table
print("\nAWS Cost Breakdown (Last 12 Months):\n")
print(tabulate(costs, headers=['Service', 'Total Cost ($)'], tablefmt='pretty'))
print(f"\nTotal Cost: ${total_cost:.2f}")

# OPTIONAL: Export to CSV
with open('aws_costs.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Service', 'Total Cost ($)'])
    writer.writerows(costs)

print("\nCSV exported as aws_costs.csv")