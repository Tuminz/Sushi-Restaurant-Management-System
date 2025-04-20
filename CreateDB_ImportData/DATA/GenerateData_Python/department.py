import csv
from faker import Faker

# Khởi tạo Faker với hỗ trợ tiếng Việt
fake = Faker("vi_VN")

# Đường dẫn tới file restaurant_branch_data.csv
restaurant_branch_file = "restaurant_branch_data.csv"

# Đọc branch_id từ file restaurant_branch_data.csv
def read_branch_ids(file_path):
    branch_ids = []
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                branch_ids.append(row["BRANCH_ID"])
    except FileNotFoundError:
        print(f"File {file_path} không tồn tại. Hãy kiểm tra lại đường dẫn.")
    return branch_ids

# Tạo dữ liệu DEPARTMENT
def generate_department_data(branch_ids, department_names, output_file):
    departments = []
    department_id_counter = 1

    for branch_id in branch_ids:
        for department_name in department_names:
            department_id = f"D{department_id_counter:03d}"
            departments.append({
                "DEPARTMENT_ID": department_id,
                "DEPARTMENT_NAME": department_name,
                "BRANCH_ID": branch_id,
            })
            department_id_counter += 1

    # Ghi dữ liệu xuống file CSV
    with open(output_file, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["DEPARTMENT_ID", "DEPARTMENT_NAME", "BRANCH_ID"])
        writer.writeheader()
        writer.writerows(departments)

    print(f"Dữ liệu đã được ghi vào {output_file}")

if __name__ == "__main__":
    # Các tên phòng ban
    department_names = [
        "Nhân viên giao hàng",
        "Lễ tân",
        "Thu ngân",
        "Đầu bếp",
        "Phụ bếp",
        "Phục vụ bàn",
        "Quản lý chi nhánh",
    ]

    # Đọc branch_id từ file CSV
    branch_ids = read_branch_ids(restaurant_branch_file)

    if branch_ids:
        # Tạo dữ liệu và ghi vào file department_data.csv
        generate_department_data(branch_ids, department_names, "department_data.csv")