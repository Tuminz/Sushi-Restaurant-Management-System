import csv
import random
from faker import Faker

# Tên file chứa dữ liệu RESTAURANT_BRANCH
restaurant_branch_file = "restaurant_branch_data.csv"
# Tên file output CSV
output_file = "table_data.csv"

# Khởi tạo Faker
faker = Faker()

# Đọc dữ liệu branch_id từ file restaurant_branch_data.csv
def get_branch_ids(file_path):
    branch_ids = []
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            branch_ids.append(row["BRANCH_ID"].strip())
    return branch_ids

# Tạo dữ liệu cho bảng TABLE_
def generate_table_data(branch_ids):
    table_data = []
    for branch_id in branch_ids:
        for table_num in range(1, 51):
            # Xác định table_status với xác suất: 45% Đang phục vụ, 35% Còn trống, 20% Được đặt trước
            table_status = random.choices(
                ["Đang phục vụ", "Còn trống", "Được đặt trước"],
                weights=[45, 35, 20],
                k=1
            )[0]

            # Xác định số ghế có sẵn
            seat_available = 5 if table_num <= 25 else 10

            # Thêm bản ghi vào danh sách
            table_data.append({
                "TABLE_NUM": table_num,
                "BRANCH_ID": branch_id,
                "TABLE_STATUS": table_status,
                "SEAT_AVAILABLE": seat_available
            })
    return table_data

# Ghi dữ liệu xuống file CSV
def write_to_csv(file_path, data):
    with open(file_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["TABLE_NUM", "BRANCH_ID", "TABLE_STATUS", "SEAT_AVAILABLE"])
        writer.writeheader()
        writer.writerows(data)

# Main
if __name__ == "__main__":
    # Đọc branch_id từ file restaurant_branch_data.csv
    branch_ids = get_branch_ids(restaurant_branch_file)

    # Tạo dữ liệu cho bảng TABLE_
    table_data = generate_table_data(branch_ids)

    # Ghi dữ liệu xuống file CSV
    write_to_csv(output_file, table_data)

    print(f"Dữ liệu đã được ghi xuống file {output_file} thành công.")