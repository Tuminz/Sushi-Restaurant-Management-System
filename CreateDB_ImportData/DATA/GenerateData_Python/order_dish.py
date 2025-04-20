import random
import csv

# Đọc dữ liệu từ các file CSV
order_file = "order_data.csv"  # Đường dẫn tới file ORDER
dish_file = "dish_available_data.csv"  # Đường dẫn tới file Dish_Available

# Đọc dữ liệu từ file order_data.csv (ORDER)
orders = []
with open(order_file, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        orders.append({
            "ORDER_ID": row["ORDER_ID"],
            "ORDER_TYPE": row["ORDER_TYPE"],
            "BRANCH_ID": row["BRANCH_ID"]
        })

# Đọc dữ liệu từ file dish_available_data.csv (Dish_Available)
dishes = []
with open(dish_file, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Lọc chỉ các món ăn có is_available = 1 và có thể giao nếu là Delivery
        if row["IS_AVAILABLE"] == "1":
            if row["IS_DELIVERABLE"] == "1" or row["IS_DELIVERABLE"] == "0":
                dishes.append({
                    "DISH_ID": row["DISH_ID"],
                    "BRANCH_ID": row["BRANCH_ID"],
                    "IS_AVAILABLE": row["IS_AVAILABLE"],
                    "ABLE_DELIVERIED": row["IS_DELIVERABLE"]
                })

# Kiểm tra xem dữ liệu có rỗng không trước khi sử dụng random.choice
if not orders:
    print("Error: No order data available.")
    exit(1)

if not dishes:
    print("Error: No available dishes data available.")
    exit(1)

# Tạo dữ liệu cho bảng ORDER_DISH
order_dish_data = []

# Mỗi ORDER_ID sẽ có ít nhất một DISH_ID hợp lệ
for order in orders:
    order_id = order["ORDER_ID"]
    order_type = order["ORDER_TYPE"]
    branch_id = order["BRANCH_ID"]

    # Lọc các món ăn hợp lệ (cùng BRANCH_ID và nếu order_type = Delivery thì thêm yêu cầu able_deliveried = 1)
    valid_dishes = [dish for dish in dishes if dish["BRANCH_ID"] == branch_id]
    
    if order_type == "Delivery":
        valid_dishes = [dish for dish in valid_dishes if dish["ABLE_DELIVERIED"] == "1"]

    if valid_dishes:
        # Chọn ngẫu nhiên một món ăn hợp lệ
        dish = random.choice(valid_dishes)
        dish_id = dish["DISH_ID"]
        # Chọn số lượng ngẫu nhiên từ 1 đến 10
        quantity = random.randint(1, 10)

        # Thêm vào danh sách dữ liệu cho ORDER_DISH
        order_dish_data.append([order_id, dish_id, quantity])

# Xuất dữ liệu vào file CSV
order_dish_file = "order_dish_data.csv"
with open(order_dish_file, mode="w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    # Ghi tiêu đề cột
    writer.writerow(["ORDER_ID", "DISH_ID", "QUANTITY"])
    # Ghi dữ liệu
    writer.writerows(order_dish_data)

print(f"Dữ liệu bảng ORDER_DISH đã được tạo và lưu tại {order_dish_file}")
