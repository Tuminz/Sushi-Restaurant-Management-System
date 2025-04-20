import csv
import random
from datetime import datetime, timedelta, time
from faker import Faker

fake = Faker()

# Constants
ORDER_COUNT = 101000
ORDER_FILE = 'order_data.csv'
CUSTOMER_FILE = 'customer_data.csv'
WORK_HISTORY_FILE = 'work_history_data.csv'
BRANCH_FILE = 'restaurant_branch_data.csv'
ORDER_TYPES = ['Online', 'Offline', 'Delivery']

# Helper functions
def generate_order_id(index):
    return f"O{index:06d}"

def random_time_within(open_time, close_time):
    """
    Generate a random time within the range open_time < order_time < close_time - 1 hour.
    """
    open_seconds = open_time.hour * 3600 + open_time.minute * 60 + open_time.second
    adjusted_close_time = (datetime.combine(datetime.today(), close_time) - timedelta(hours=1)).time()
    close_seconds = adjusted_close_time.hour * 3600 + adjusted_close_time.minute * 60 + adjusted_close_time.second

    if close_seconds <= open_seconds:
        raise ValueError("Invalid time range: close_time must be at least 1 hour after open_time.")

    random_seconds = random.randint(open_seconds + 1, close_seconds - 1)
    return time(random_seconds // 3600, (random_seconds % 3600) // 60, random_seconds % 60)

# Load data from CSV files
def load_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_csv(file_path, data, fieldnames):
    with open(file_path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

customers = load_csv(CUSTOMER_FILE)
work_history = load_csv(WORK_HISTORY_FILE)
branches = load_csv(BRANCH_FILE)

# Process branch open/close times
branch_times = {
    branch['BRANCH_ID']: {
        'open_time': datetime.strptime(branch['OPEN_TIME'], '%H:%M:%S').time(),
        'close_time': datetime.strptime(branch['CLOSE_TIME'], '%H:%M:%S').time()
    }
    for branch in branches
}

# Generate orders
orders = []
work_history_cycle = iter(work_history)
branch_order_types = {branch['BRANCH_ID']: set() for branch in branches}

for i in range(1, ORDER_COUNT + 1):
    order_id = generate_order_id(i)
    customer = customers[(i - 1) % len(customers)]
    customer_id = customer['CUSTOMER_ID']

    # Cycle through work history to find valid branch and date
    while True:
        try:
            work_record = next(work_history_cycle)
        except StopIteration:
            work_history_cycle = iter(work_history)
            work_record = next(work_history_cycle)

        branch_start_date = datetime.strptime(work_record['BRANCH_START_DATE'], '%Y-%m-%d').date()
        branch_end_date = (
            datetime.strptime(work_record['BRANCH_END_DATE'], '%Y-%m-%d').date()
            if work_record['BRANCH_END_DATE'] else datetime.today().date()
        )

        if branch_start_date <= datetime.today().date() <= branch_end_date:
            order_date = fake.date_between(start_date=branch_start_date, end_date=branch_end_date)
            branch_id = work_record['BRANCH_ID']
            break

    # Ensure all order types are covered
    if len(branch_order_types[branch_id]) < len(ORDER_TYPES):
        available_types = set(ORDER_TYPES) - branch_order_types[branch_id]
        order_type = random.choice(list(available_types))
        branch_order_types[branch_id].add(order_type)
    else:
        order_type = random.choice(ORDER_TYPES)

    # Generate order time
    open_time = branch_times[branch_id]['open_time']
    close_time = branch_times[branch_id]['close_time']
    order_time = random_time_within(open_time, close_time)

    # Append order data
    orders.append({
        'ORDER_ID': order_id,
        'ORDER_DATE': order_date.isoformat(),  # Use ISO 8601 format (YYYY-MM-DD)
        'BRANCH_ID': branch_id,
        'CUSTOMER_ID': customer_id,
        'ORDER_TYPE': order_type,
        'ORDER_TIME': order_time.strftime('%H:%M:%S')
    })

# Write to CSV
order_fieldnames = ['ORDER_ID', 'ORDER_DATE', 'BRANCH_ID', 'CUSTOMER_ID', 'ORDER_TYPE', 'ORDER_TIME']
write_csv(ORDER_FILE, orders, order_fieldnames)

print(f"Generated {ORDER_COUNT} orders and saved to {ORDER_FILE}.")
