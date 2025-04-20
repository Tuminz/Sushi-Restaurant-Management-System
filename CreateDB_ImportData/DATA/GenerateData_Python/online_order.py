"""import csv
import random
from datetime import datetime, timedelta
from faker import Faker

# Khởi tạo Faker
fake = Faker()

# Đường dẫn đến các file dữ liệu cần thiết
order_file = 'order_data.csv'
restaurant_branch_file = 'restaurant_branch_data.csv'
table_file = 'table_data.csv'
online_order_file = 'online_order_data.csv'

# Hàm đọc dữ liệu từ file CSV
def read_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

# Đọc dữ liệu từ các file
order_data = read_csv(order_file)
restaurant_branch_data = read_csv(restaurant_branch_file)
table_data = read_csv(table_file)

# Tạo dữ liệu cho bảng ONLINE_ORDER
online_order_data = []
current_date = datetime.now().date()

for order in order_data:
    if order['ORDER_TYPE'] != 'Online':
        continue

    oorder_id = order['ORDER_ID']
    order_date = datetime.strptime(order['ORDER_DATE'], '%Y-%m-%d').date()
    order_time = datetime.strptime(order['ORDER_TIME'], '%H:%M:%S').time()

    # arrival_date: Random trong khoảng order_date < arrival_date <= order_date + 7 ngày
    arrival_date = order_date + timedelta(days=random.randint(1, 7))

    # arrival_time: Random giữa order_time và close_time - 1 giờ
    branch_id = order['BRANCH_ID']
    branch = next((b for b in restaurant_branch_data if b['BRANCH_ID'] == branch_id), None)
    if not branch:
        continue

    close_time = datetime.strptime(branch['CLOSE_TIME'], '%H:%M:%S').time()
    max_arrival_time = (datetime.combine(current_date, close_time) - timedelta(hours=1)).time()

    arrival_time = fake.date_time_between_dates(
        datetime_start=datetime.combine(current_date, order_time),
        datetime_end=datetime.combine(current_date, max_arrival_time)
    ).time()

    # table_number: Lựa chọn dựa trên arrival_date
    tables_in_branch = [t for t in table_data if t['BRANCH_ID'] == branch_id]

    if arrival_date == current_date:
        tables_in_branch = [t for t in tables_in_branch if t['TABLE_STATUS'] == 'ĐƯỢC ĐẶT TRƯỚC']

    # Kiểm tra nếu danh sách rỗng
    if not tables_in_branch:
        print(f"Warning: No available tables for BRANCH_ID={branch_id} and ARRIVAL_DATE={arrival_date}")
        continue

    # Chọn một bàn ngẫu nhiên
    table = random.choice(tables_in_branch)
    table_number = int(table['TABLE_NUM'])

    # customer_quantity: Random dựa trên table_number
    if 1 <= table_number <= 25:
        customer_quantity = random.randint(1, 5)
    elif 26 <= table_number <= 50:
        customer_quantity = random.randint(6, 10)
    else:
        continue

    # Thêm dữ liệu vào danh sách
    online_order_data.append({
        'OORDER_ID': oorder_id,
        'ARRIVAL_DATE': arrival_date.strftime('%Y-%m-%d'),
        'ARRIVAL_TIME': arrival_time.strftime('%H:%M:%S'),
        'TABLE_NUMBER': table_number,
        'BRANCH_ID': branch_id,
        'CUSTOMER_QUANTITY': customer_quantity,
    })

# Ghi dữ liệu xuống file CSV
with open(online_order_file, mode='w', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['OORDER_ID', 'ARRIVAL_DATE', 'ARRIVAL_TIME', 'TABLE_NUMBER', 'BRANCH_ID', 'CUSTOMER_QUANTITY'])
    writer.writeheader()
    writer.writerows(online_order_data)

print(f"Dữ liệu đã được ghi vào file {online_order_file}")

"""
'''
import csv
import random
from datetime import datetime, timedelta
from faker import Faker
import os

# Khởi tạo Faker
fake = Faker()

# Hàm đọc dữ liệu từ file CSV
def read_csv(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} không tồn tại. Vui lòng kiểm tra đường dẫn.")
    data = []
    with open(file_path, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# Đọc dữ liệu từ các file CSV
order_data = read_csv("order_data.csv")
restaurant_branch_data = read_csv("restaurant_branch_data.csv")
table_data = read_csv("table_data.csv")

# Hàm tạo thời gian đến (arrival_time)
def generate_arrival_time(order_time, open_time, close_time, arrival_date, order_date):
    # Chuyển đổi chuỗi thời gian có giây (HH:MM:SS)
    order_time_obj = datetime.strptime(order_time, "%H:%M:%S").time()
    open_time_obj = datetime.strptime(open_time, "%H:%M:%S").time()
    close_time_obj = datetime.strptime(close_time, "%H:%M:%S").time()

    if arrival_date == order_date:
        # Nếu arrival_date trùng với order_date, chọn thời gian sau order_time và trước close_time
        while True:
            random_time = fake.time_object(end_datetime=close_time_obj)
            if random_time > order_time_obj:
                return random_time
    else:
        # Nếu arrival_date khác order_date, chọn thời gian trong khoảng từ open_time đến close_time
        while True:
            random_time = fake.time_object()
            if open_time_obj <= random_time <= close_time_obj:
                return random_time

# Tạo dữ liệu cho bảng ONLINE_ORDER
online_order_data = []

# Lặp qua các đơn hàng có order_type là Online
for order in order_data:
    if order["ORDER_TYPE"] == "Online":
        oorder_id = order["ORDER_ID"]
        order_date = datetime.strptime(order["ORDER_DATE"], "%Y-%m-%d").date()
        order_time = order["ORDER_TIME"]
        branch_id = order["BRANCH_ID"]

        # Lấy thông tin từ bảng restaurant_branch_data
        branch_info = next((branch for branch in restaurant_branch_data if branch["BRANCH_ID"] == branch_id), None)
        if not branch_info:
            continue  # Nếu không tìm thấy thông tin chi nhánh, bỏ qua

        open_time = branch_info["OPEN_TIME"]
        close_time = branch_info["CLOSE_TIME"]

        # Tạo arrival_date, thời gian này phải lớn hơn order_date và nhỏ hơn hoặc bằng order_date + 7 ngày
        arrival_date = order_date + timedelta(days=random.randint(1, 7))

        # Tạo arrival_time dựa trên điều kiện đã mô tả
        arrival_time = generate_arrival_time(order_time, open_time, close_time, arrival_date, order_date)

        # Lấy table_number từ bảng table_data
        if arrival_date == datetime.today().date():
            # Nếu arrival_date là ngày hôm nay, chọn table_number với status "ĐƯỢC ĐẶT TRƯỚC"
            available_tables = [table for table in table_data if table["BRANCH_ID"] == branch_id and table["TABLE_STATUS"] == "ĐƯỢC ĐẶT TRƯỚC"]
        else:
            # Nếu arrival_date không phải ngày hôm nay, chọn bất kỳ table_number nào
            available_tables = [table for table in table_data if table["BRANCH_ID"] == branch_id]

        # Chuyển table_number thành kiểu int trước khi sử dụng
        if available_tables:
            table_number = int(random.choice(available_tables)["TABLE_NUM"])  # Chuyển sang int
        else:
            continue  # Nếu không có bảng phù hợp, bỏ qua

        # Tính customer_quantity theo table_number
        if 1 <= table_number <= 25:
            customer_quantity = random.randint(1, 5)
        elif 26 <= table_number <= 50:
            customer_quantity = random.randint(6, 10)
        else:
            continue  # Nếu table_number không hợp lệ, bỏ qua

        # Thêm thông tin vào danh sách online_order_data
        online_order_data.append({
            "OORDER_ID": oorder_id,
            "ARRIVAL_DATE": arrival_date.strftime("%Y-%m-%d"),
            "ARRIVAL_TIME": arrival_time.strftime("%H:%M"),
            "TABLE_NUMBER": table_number,
            "BRANCH_ID": branch_id,
            "CUSTOMER_QUANTITY": customer_quantity,
        })

# Ghi dữ liệu xuống file CSV
with open("online_order_data.csv", "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["OORDER_ID", "ARRIVAL_DATE", "ARRIVAL_TIME", "TABLE_NUMBER", "BRANCH_ID", "CUSTOMER_QUANTITY"])
    writer.writeheader()
    writer.writerows(online_order_data)

print("Dữ liệu đã được ghi xuống file online_order_data.csv")
'''
import csv
import random
from datetime import datetime, timedelta
from faker import Faker
import os

# Khởi tạo Faker
fake = Faker()

# Hàm đọc dữ liệu từ file CSV
def read_csv(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} không tồn tại. Vui lòng kiểm tra đường dẫn.")
    data = []
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# Đọc dữ liệu từ các file CSV
order_data = read_csv("order_data.csv")
restaurant_branch_data = read_csv("restaurant_branch_data.csv")
table_data = read_csv("table_data.csv")

# Tạo dữ liệu cho bảng ONLINE_ORDER
online_order_data = []

# Lấy danh sách các đơn hàng có order_type là Online
online_orders = [order for order in order_data if order["ORDER_TYPE"] == "Online"]

# Duyệt qua từng đơn hàng và tạo dữ liệu độc lập
for order in online_orders:
    # Lấy thông tin từ bảng ORDER
    oorder_id = order["ORDER_ID"]
    print(f"Processing order ID: {oorder_id}")

    order_date = datetime.strptime(order["ORDER_DATE"], "%Y-%m-%d").date()
    order_time = datetime.strptime(order["ORDER_TIME"], "%H:%M:%S").time()
    branch_id = order["BRANCH_ID"]

    # Lấy thông tin từ bảng RESTAURANT_BRANCH
    branch_info = next((branch for branch in restaurant_branch_data if branch["BRANCH_ID"] == branch_id), None)
    if not branch_info:
        print(f"Branch ID {branch_id} not found. Skipping order ID {oorder_id}.")
        continue

    open_time = datetime.strptime(branch_info["OPEN_TIME"], "%H:%M:%S").time()
    close_time = datetime.strptime(branch_info["CLOSE_TIME"], "%H:%M:%S").time()

    # Tạo arrival_date
    arrival_date = order_date + timedelta(days=random.randint(1, 7))
    print(f"Arrival date for order ID {oorder_id}: {arrival_date}")

    # Tạo arrival_time
    if arrival_date == order_date:
        while True:
            random_time = fake.time_object(end_datetime=datetime.combine(order_date, close_time))
            if random_time > order_time:
                arrival_time = random_time
                break
    else:
        while True:
            random_time = fake.time_object()
            if open_time <= random_time <= close_time:
                arrival_time = random_time
                break
    print(f"Arrival time for order ID {oorder_id}: {arrival_time}")

    # Lấy thông tin table_number từ bảng TABLE
    available_tables = [
        table for table in table_data
        if table["BRANCH_ID"] == branch_id
    ]

    if available_tables:
        table_number = int(random.choice(available_tables)["TABLE_NUM"])
    else:
        print(f"No available tables for order ID {oorder_id}. Skipping.")
        continue
    print(f"Table number for order ID {oorder_id}: {table_number}")

    # Xác định customer_quantity theo table_number
    if 1 <= table_number <= 25:
        customer_quantity = random.randint(1, 5)
    elif 26 <= table_number <= 50:
        customer_quantity = random.randint(6, 10)
    else:
        print(f"Invalid table number {table_number} for order ID {oorder_id}. Skipping.")
        continue
    print(f"Customer quantity for order ID {oorder_id}: {customer_quantity}")

    # Thêm thông tin vào danh sách online_order_data
    online_order_data.append({
        "OORDER_ID": oorder_id,
        "ARRIVAL_DATE": arrival_date.strftime("%Y-%m-%d"),
        "ARRIVAL_TIME": arrival_time.strftime("%H:%M:%S"),
        "TABLE_NUMBER": table_number,
        "BRANCH_ID": branch_id,
        "CUSTOMER_QUANTITY": customer_quantity,
    })

# Ghi dữ liệu xuống file CSV
with open("online_order_data.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["OORDER_ID", "ARRIVAL_DATE", "ARRIVAL_TIME", "TABLE_NUMBER", "BRANCH_ID", "CUSTOMER_QUANTITY"])
    writer.writeheader()
    writer.writerows(online_order_data)

print("Dữ liệu đã được ghi xuống file online_order_data.csv")



