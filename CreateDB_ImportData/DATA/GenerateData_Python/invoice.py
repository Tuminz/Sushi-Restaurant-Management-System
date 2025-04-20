'''
import csv
import random
from datetime import datetime, timedelta

# Đường dẫn tới các file CSV đầu vào
order_file = "order_data.csv"
oorder_file = "online_order_data.csv"
dorder_file = "delivery_order_data.csv"

# Đọc dữ liệu từ file order_data.csv (Order)
orders = []
with open(order_file, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        orders.append({
            "ORDER_ID": row["ORDER_ID"],
            "ORDER_TYPE": row["ORDER_TYPE"],
            "ORDER_DATE": row["ORDER_DATE"],
            "ORDER_TIME": row["ORDER_TIME"]
        })

# Đọc dữ liệu từ file oorder_data.csv (Online Order)
oorders = {}
with open(oorder_file, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        oorders[row["OORDER_ID"]] = {
            "ARRIVAL_DATE": row["ARRIVAL_DATE"],
            "ARRIVAL_TIME": row["ARRIVAL_TIME"]
        }

# Đọc dữ liệu từ file dorder_data.csv (Delivery Order)
dorders = {}
with open(dorder_file, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        dorders[row["DORDER_ID"]] = {
            "DATE_DELIVERY": row["DATE_DELIVERY"],
            "TIME_DELIVERY": row["TIME_DELIVERY"]
        }

# Tạo dữ liệu cho bảng INVOICE
invoice_data = []
for i in range(1, 100001):
    invoice_id = f"I{i:06d}"

    # Chọn ngẫu nhiên một order_id
    order = random.choice(orders)
    order_id = order["ORDER_ID"]
    order_type = order["ORDER_TYPE"]
    order_date = datetime.strptime(order["ORDER_DATE"], "%Y-%m-%d")
    order_time = datetime.strptime(order["ORDER_TIME"], "%H:%M:%S")

    # Xử lý issue_date và issue_time
    if order_type == "Offline":
        issue_date = order_date
        issue_time = order_time
    elif order_type == "Online":
        oorder = oorders.get(order_id, None)
        if oorder:
            max_date = datetime.strptime(oorder["ARRIVAL_DATE"], "%Y-%m-%d")
            issue_date = order_date + timedelta(days=random.randint(0, (max_date - order_date).days))

            max_time = datetime.strptime(oorder["ARRIVAL_TIME"], "%H:%M:%S")
            issue_time = order_time + timedelta(minutes=random.randint(0, int((max_time - order_time).total_seconds() // 60)))
    elif order_type == "Delivery":
        dorder = dorders.get(order_id, None)
        if dorder:
            max_date = datetime.strptime(dorder["DATE_DELIVERY"], "%Y-%m-%d")
            issue_date = order_date + timedelta(days=random.randint(0, (max_date - order_date).days))

            max_time = datetime.strptime(dorder["TIME_DELIVERY"], "%H:%M:%S")
            issue_time = order_time + timedelta(minutes=random.randint(0, int((max_time - order_time).total_seconds() // 60)))

    # Gán mặc định nếu không tìm thấy dữ liệu liên quan
    if "issue_date" not in locals():
        issue_date = order_date
    if "issue_time" not in locals():
        issue_time = order_time

    # Định dạng issue_date và issue_time
    issue_date_str = issue_date.strftime("%Y-%m-%d")
    issue_time_str = issue_time.strftime("%H:%M:%S")

    # Gán giá trị cố định cho discount_amount và final_amount
    discount_amount = 0
    final_amount = 0

    # Thêm dữ liệu vào danh sách
    invoice_data.append([invoice_id, final_amount, discount_amount, issue_date_str, issue_time_str, order_id])

# Xuất dữ liệu vào file CSV
invoice_file = "invoice_data.csv"
try:
    with open(invoice_file, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        # Ghi tiêu đề cột
        writer.writerow(["INVOICE_ID", "FINAL_AMOUNT", "DISCOUNT_AMOUNT", "ISSUE_DATE", "ISSUE_TIME", "ORDER_ID"])
        # Ghi dữ liệu
        writer.writerows(invoice_data)
    print(f"Dữ liệu bảng INVOICE đã được tạo và lưu tại {invoice_file}")
except Exception as e:
    print(f"Lỗi khi ghi file: {e}")
'''
import csv
import random
from datetime import datetime, timedelta

# Đường dẫn tới các file CSV đầu vào
order_file = "order_data.csv"
oorder_file = "online_order_data.csv"
dorder_file = "delivery_order_data.csv"
branch_file = "restaurant_branch_data.csv"

# Đọc dữ liệu từ file order_data.csv (Order)
orders = []
with open(order_file, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        orders.append({
            "ORDER_ID": row["ORDER_ID"],
            "ORDER_TYPE": row["ORDER_TYPE"],
            "ORDER_DATE": row["ORDER_DATE"],
            "ORDER_TIME": row["ORDER_TIME"],
            "BRANCH_ID": row["BRANCH_ID"]
        })

# Đọc dữ liệu từ file oorder_data.csv (Online Order)
oorders = {}
with open(oorder_file, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        oorders[row["OORDER_ID"]] = {
            "ARRIVAL_DATE": row["ARRIVAL_DATE"],
            "ARRIVAL_TIME": row["ARRIVAL_TIME"]
        }

# Đọc dữ liệu từ file dorder_data.csv (Delivery Order)
dorders = {}
with open(dorder_file, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        dorders[row["DORDER_ID"]] = {
            "DATE_DELIVERY": row["DATE_DELIVERY"],
            "TIME_DELIVERY": row["TIME_DELIVERY"]
        }

# Đọc dữ liệu từ file restaurant_branch_data.csv (Restaurant Branch)
branches = {}
with open(branch_file, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        branches[row["BRANCH_ID"]] = {
            "OPEN_TIME": row["OPEN_TIME"],
            "CLOSE_TIME": row["CLOSE_TIME"]
        }

# Tạo dữ liệu cho bảng INVOICE
invoice_data = []
for i in range(1, 101001):
    invoice_id = f"I{i:06d}"

    # Chọn ngẫu nhiên một order_id
    order = random.choice(orders)
    order_id = order["ORDER_ID"]
    order_type = order["ORDER_TYPE"]
    order_date = datetime.strptime(order["ORDER_DATE"], "%Y-%m-%d")
    order_time = datetime.strptime(order["ORDER_TIME"], "%H:%M:%S")
    branch_id = order["BRANCH_ID"]

    open_time = datetime.strptime(branches[branch_id]["OPEN_TIME"], "%H:%M:%S")
    close_time = datetime.strptime(branches[branch_id]["CLOSE_TIME"], "%H:%M:%S")

    # Xử lý issue_date và issue_time
    if order_type == "Offline":
        issue_date = order_date
        issue_time = order_time
    elif order_type == "Online":
        oorder = oorders.get(order_id, None)
        if oorder:
            max_date = datetime.strptime(oorder["ARRIVAL_DATE"], "%Y-%m-%d")
            issue_date = order_date + timedelta(days=random.randint(0, (max_date - order_date).days))

            if issue_date == order_date:
                issue_time = order_time + timedelta(minutes=random.randint(0, int((close_time - order_time).total_seconds() // 60)))
            elif issue_date == max_date:
                max_time = datetime.strptime(oorder["ARRIVAL_TIME"], "%H:%M:%S")
                issue_time = open_time + timedelta(minutes=random.randint(0, int((max_time - open_time).total_seconds() // 60)))
            else:
                issue_time = open_time + timedelta(minutes=random.randint(0, int((close_time - open_time).total_seconds() // 60)))
    elif order_type == "Delivery":
        dorder = dorders.get(order_id, None)
        if dorder:
            max_date = datetime.strptime(dorder["DATE_DELIVERY"], "%Y-%m-%d")
            issue_date = order_date + timedelta(days=random.randint(0, (max_date - order_date).days))

            if issue_date == order_date:
                issue_time = order_time + timedelta(minutes=random.randint(0, int((close_time - order_time).total_seconds() // 60)))
            elif issue_date == max_date:
                max_time = datetime.strptime(dorder["TIME_DELIVERY"], "%H:%M:%S")
                issue_time = open_time + timedelta(minutes=random.randint(0, int((max_time - open_time).total_seconds() // 60)))
            else:
                issue_time = open_time + timedelta(minutes=random.randint(0, int((close_time - open_time).total_seconds() // 60)))

    # Định dạng issue_date và issue_time
    issue_date_str = issue_date.strftime("%Y-%m-%d")
    issue_time_str = issue_time.strftime("%H:%M:%S")

    # Gán giá trị cố định cho discount_amount và final_amount
    discount_amount = 0
    final_amount = 0

    # Thêm dữ liệu vào danh sách
    invoice_data.append([invoice_id, final_amount, discount_amount, issue_date_str, issue_time_str, order_id])

# Xuất dữ liệu vào file CSV
invoice_file = "invoice_data.csv"
try:
    with open(invoice_file, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        # Ghi tiêu đề cột
        writer.writerow(["INVOICE_ID", "FINAL_AMOUNT", "DISCOUNT_AMOUNT", "ISSUE_DATE", "ISSUE_TIME", "ORDER_ID"])
        # Ghi dữ liệu
        writer.writerows(invoice_data)
    print(f"Dữ liệu bảng INVOICE đã được tạo và lưu tại {invoice_file}")
except Exception as e:
    print(f"Lỗi khi ghi file: {e}")
