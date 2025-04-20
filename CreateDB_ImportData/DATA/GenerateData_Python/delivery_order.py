"""import csv
import random
from datetime import datetime, timedelta

# Đọc dữ liệu từ các file CSV
order_file = "order_data.csv"  # Đường dẫn tới file ORDER
branch_file = "restaurant_branch_data.csv"  # Đường dẫn tới file Restaurant_branch

# Đọc dữ liệu từ file order_data.csv (ORDER)
orders = []
with open(order_file, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row["ORDER_TYPE"] == "Delivery":  # Chỉ lấy các đơn hàng Delivery
            orders.append({
                "ORDER_ID": row["ORDER_ID"],
                "ORDER_DATE": row["ORDER_DATE"],
                "ORDER_TIME": row["ORDER_TIME"],
                "BRANCH_ID": row["BRANCH_ID"]
            })

# Đọc dữ liệu từ file restaurant_branch_data.csv (Restaurant_branch)
branches = {}
with open(branch_file, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        branches[row["BRANCH_ID"]] = {
            "CLOSE_TIME": row["CLOSE_TIME"]
        }

# Kiểm tra xem dữ liệu có rỗng không trước khi sử dụng random.choice
if not orders:
    print("Error: No delivery orders data available.")
    exit(1)

if not branches:
    print("Error: No branch data available.")
    exit(1)

# Tạo dữ liệu cho bảng DELIVERY_ORDER
delivery_order_data = []

# Mỗi ORDER_ID có thể có một DELIVERY_ORDER
for order in orders:
    order_id = order["ORDER_ID"]
    order_date = datetime.strptime(order["ORDER_DATE"], "%Y-%m-%d")
    order_time = datetime.strptime(order["ORDER_TIME"], "%H:%M:%S")
    branch_id = order["BRANCH_ID"]

    # Tính toán date_delivery trong khoảng từ order_date đến order_date + 7 ngày
    max_delivery_date = order_date + timedelta(days=7)
    date_delivery = order_date + timedelta(days=random.randint(1, 7))  # Random trong khoảng 1 đến 7 ngày

    # Lấy giờ đóng cửa của chi nhánh
    close_time_str = branches[branch_id]["CLOSE_TIME"]
    close_time = datetime.strptime(close_time_str, "%H:%M:%S")

    # Tạo time_delivery, đảm bảo thời gian giao hàng phải sau order_time và trước close_time
    while True:
        random_minutes = random.randint(1, int((close_time - order_time).total_seconds() // 60))
        time_delivery = order_time + timedelta(minutes=random_minutes)
        if time_delivery < close_time:
            break

    # Chuyển time_delivery thành định dạng thời gian cho SQL
    time_delivery_str = time_delivery.strftime("%H:%M:%S")
    date_delivery_str = date_delivery.strftime("%Y-%m-%d")

    # Thêm dữ liệu vào danh sách
    delivery_order_data.append([order_id, time_delivery_str, date_delivery_str])

# Xuất dữ liệu vào file CSV
delivery_order_file = "delivery_order_data.csv"
with open(delivery_order_file, mode="w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    # Ghi tiêu đề cột
    writer.writerow(["DORDER_ID", "TIME_DELIVERY", "DATE_DELIVERY"])
    # Ghi dữ liệu
    writer.writerows(delivery_order_data)

print(f"Dữ liệu bảng DELIVERY_ORDER đã được tạo và lưu tại {delivery_order_file}")
"""

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

# Hàm tạo thời gian giao hàng (time_delivery)
def generate_time_delivery(order_time, open_time, close_time, date_delivery, order_date):
    # Chuyển đổi chuỗi thời gian có giây (HH:MM:SS)
    order_time_obj = datetime.strptime(order_time, "%H:%M:%S").time()  # Sửa lại định dạng
    open_time_obj = datetime.strptime(open_time, "%H:%M:%S").time()  # Sửa lại định dạng
    close_time_obj = datetime.strptime(close_time, "%H:%M:%S").time()  # Sửa lại định dạng

    if date_delivery == order_date:
        # Nếu ngày giao hàng là ngày đặt hàng, thì chọn giờ giao hàng sau order_time và trước close_time của nhà hàng
        while True:
            random_time = fake.time_object(end_datetime=close_time_obj)
            if random_time > order_time_obj:
                return random_time
    else:
        # Nếu ngày giao hàng khác ngày đặt hàng, chọn thời gian trong khoảng từ open_time đến close_time của nhà hàng
        while True:
            random_time = fake.time_object()
            if open_time_obj <= random_time <= close_time_obj:
                return random_time

# Tạo dữ liệu cho bảng DELIVERY_ORDER
delivery_data = []

# Lặp qua các đơn hàng có order_type là Delivery
for order in order_data:
    if order["ORDER_TYPE"] == "Delivery":
        dorder_id = order["ORDER_ID"]
        order_date = datetime.strptime(order["ORDER_DATE"], "%Y-%m-%d").date()
        order_time = order["ORDER_TIME"]
        branch_id = order["BRANCH_ID"]

        # Lấy thông tin từ bảng restaurant_branch_data
        branch_info = next((branch for branch in restaurant_branch_data if branch["BRANCH_ID"] == branch_id), None)
        if not branch_info:
            continue  # Nếu không tìm thấy thông tin chi nhánh, bỏ qua

        open_time = branch_info["OPEN_TIME"]
        close_time = branch_info["CLOSE_TIME"]

        # Tạo date_delivery, thời gian này phải lớn hơn order_date và nhỏ hơn hoặc bằng order_date + 7 ngày
        date_delivery = order_date + timedelta(days=random.randint(1, 7))

        # Tạo time_delivery dựa trên điều kiện đã mô tả
        time_delivery = generate_time_delivery(order_time, open_time, close_time, date_delivery, order_date)

        # Thêm thông tin vào danh sách delivery_data
        delivery_data.append({
            "DORDER_ID": dorder_id,
            "TIME_DELIVERY": time_delivery.strftime("%H:%M:%S"),
            "DATE_DELIVERY": date_delivery.strftime("%Y-%m-%d"),
        })

# Ghi dữ liệu xuống file CSV
with open("delivery_order_data.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["DORDER_ID", "TIME_DELIVERY", "DATE_DELIVERY"])
    writer.writeheader()
    writer.writerows(delivery_data)

print("Dữ liệu đã được ghi xuống file delivery_data.csv")


