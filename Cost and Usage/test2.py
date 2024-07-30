import boto3
import logging
from tabulate import tabulate
from typing import List, Dict

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize AWS Cost Explorer client
ce = boto3.client('ce')

def get_cost_and_usage(time_period: Dict[str, str], granularity: str, metrics: List[str], group_by: List[Dict[str, str]]) -> List[List[str]]:
	try:
		response = ce.get_cost_and_usage(
			TimePeriod=time_period,
			Granularity=granularity,
			Metrics=metrics,
			GroupBy=group_by
			# Uncomment the following line if you want to apply the filter
			# Filter=filter
		)
	except Exception as e:
		logger.error(f"Error fetching cost and usage data: {e}")
		return []

	costs = []
	for result in response['ResultsByTime']:
		for group in result['Groups']:
			costs.append([group['Keys'][0], group['Metrics']['BlendedCost']['Amount']])
	
	return costs

def calculate_total_cost(costs: List[List[str]]) -> float:
	total_cost = 0.0
	for cost in costs:
		total_cost += float(cost[1])
	return total_cost

def main():
	# Define parameters
	time_period = {
		'Start': '2024-01-01',
		'End': '2024-07-31'
	}
	granularity = 'MONTHLY'
	metrics = ['BlendedCost']
	group_by = [{'Type': 'DIMENSION', 'Key': 'SERVICE'}]

	# Get cost and usage data
	costs = get_cost_and_usage(time_period, granularity, metrics, group_by)

	if not costs:
		logger.error("No cost data retrieved.")
		return

	# Calculate total cost
	total_cost = calculate_total_cost(costs)

	# Tabulate and print the results
	print(tabulate(costs, headers=['Service', 'Cost'], tablefmt='pretty'))
	print(f"Total Cost: ${total_cost:.2f}")

if __name__ == "__main__":
	main()