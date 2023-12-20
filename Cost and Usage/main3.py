from flask import Flask, render_template
import boto3

app = Flask(__name__)

@app.route('/')
def home():
    # Create a Cost Explorer client
    ce = boto3.client('ce', region_name='us-east-1')

    # Set the time period for the query
    time_period = {
        'Start': '2023-01-01',
        'End': '2023-12-30'
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
            costs.append({
                'service': group['Keys'][0],
                'cost': group['Metrics']['BlendedCost']['Amount']
            })

    # Render the template with the costs
    return render_template('home.html', costs=costs)

if __name__ == '__main__':
    app.run(debug=True)