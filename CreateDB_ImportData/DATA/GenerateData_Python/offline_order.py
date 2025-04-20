import csv
import random
from datetime import datetime, date
from faker import Faker

fake = Faker()

# Đường dẫn tới các file CSV input
order_data_file = 'order_data.csv'
table_data_file = 'table_data.csv'
work_history_data_file = 'work_history_data.csv'

# Đường dẫn file output
output_file = 'offline_order_data.csv'

# Đọc dữ liệu từ file CSV
def read_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

order_data = read_csv(order_data_file)
table_data = read_csv(table_data_file)
work_history_data = read_csv(work_history_data_file)

# Tạo dữ liệu cho bảng OFFLINE_ORDER
offline_orders = []

# Tạo danh sách OFORDER_ID là các ORDER_ID có ORDER_TYPE = 'Offline'
offline_order_ids = [
    order['ORDER_ID'] for order in order_data if order['ORDER_TYPE'] == 'Offline'
]
print("Danh sách Offline Order IDs:", offline_order_ids)

# Tạo danh sách TABLE_NUMBER ngẫu nhiên
table_numbers = {
    branch['BRANCH_ID']: [table['TABLE_NUM'] for table in table_data if table['BRANCH_ID'] == branch['BRANCH_ID']]
    for branch in table_data
}

# Tạo danh sách EMPLOYEE_ID phù hợp
def get_eligible_employees(order):
    today = date.today().strftime('%Y-%m-%d')
    return [
        wh['EMPLOYEE_ID'] for wh in work_history_data
        if wh['BRANCH_ID'] == order['BRANCH_ID']
        and wh['BRANCH_START_DATE'] <= order['ORDER_DATE']
        and (wh['BRANCH_END_DATE'] == '' or wh['BRANCH_END_DATE'] >= order['ORDER_DATE'])
    ]

used_tables_by_branch_date_time = {}

for order_id in offline_order_ids:
    order = next(order for order in order_data if order['ORDER_ID'] == order_id)
    branch_id = order['BRANCH_ID']
    order_date_time = (order['ORDER_DATE'], order['ORDER_TIME'], branch_id)

    # Lựa chọn TABLE_NUMBER ngẫu nhiên và không trùng lặp
    if order_date_time not in used_tables_by_branch_date_time:
        used_tables_by_branch_date_time[order_date_time] = set()

    available_tables = [
        table for table in table_numbers.get(branch_id, [])
        if table not in used_tables_by_branch_date_time[order_date_time]
    ]

    if not available_tables:
        print(f"Không có bàn nào khả dụng cho order_id {order_id}")
        continue

    table_num = random.choice(available_tables)
    used_tables_by_branch_date_time[order_date_time].add(table_num)
    print(f"Chọn table_num {table_num} cho order_id {order_id}")

    # Lựa chọn EMPLOYEE_ID ngẫu nhiên
    eligible_employees = get_eligible_employees(order)
    if not eligible_employees:
        print(f"Không có nhân viên nào phù hợp cho order_id {order_id}")
        continue

    employee_id = random.choice(eligible_employees)
    print(f"Chọn employee_id {employee_id} cho order_id {order_id}")

    # Random employee_rating với tỷ lệ 70% là 5, 30% là từ 1-4
    employee_rating = 5 if random.random() < 0.7 else random.randint(1, 4)
    print(f"Chọn employee_rating {employee_rating} cho order_id {order_id}")

    offline_orders.append({
        'OFORDER_ID': order_id,
        'TABLE_NUMBER': table_num,
        'EMPLOYEE_ID': employee_id,
        'BRANCH_ID': branch_id,
        'EMPLYEE_RATING': employee_rating
    })

# Ghi dữ liệu xuống file CSV
with open(output_file, mode='w', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['OFORDER_ID', 'TABLE_NUMBER', 'EMPLOYEE_ID', 'BRANCH_ID', 'EMPLYEE_RATING'])
    writer.writeheader()
    writer.writerows(offline_orders)

print(f"Dữ liệu đã được ghi vào file {output_file}")
