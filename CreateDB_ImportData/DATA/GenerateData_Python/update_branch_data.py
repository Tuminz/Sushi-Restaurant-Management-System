import csv
from faker import Faker

# Đường dẫn tới các file CSV
restaurant_branch_file = 'restaurant_branch_data.csv'
department_file = 'department_data.csv'
employee_file = 'employee_data.csv'

# Hàm đọc dữ liệu từ file CSV
def read_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

# Hàm ghi dữ liệu vào file CSV
def write_csv(file_path, data, fieldnames):
    with open(file_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Đọc dữ liệu từ các file CSV
restaurant_branch_data = read_csv(restaurant_branch_file)
department_data = read_csv(department_file)
employee_data = read_csv(employee_file)

# Tạo từ điển department theo branch_id và tên phòng ban "Quản lý chi nhánh"
department_map = {
    dept['BRANCH_ID']: dept['DEPARTMENT_ID']
    for dept in department_data
    if dept['DEPARTMENT_NAME'] == 'Quản lý chi nhánh'
}

# Tạo từ điển employee theo department_id
employee_map = {
    emp['DEPARTMENT_ID']: emp['EMPLOYEE_ID']
    for emp in employee_data
}

# Cập nhật manager_id cho restaurant_branch_data
for branch in restaurant_branch_data:
    branch_id = branch['BRANCH_ID']
    if branch_id in department_map:
        department_id = department_map[branch_id]
        if department_id in employee_map:
            branch['MANAGER_ID'] = employee_map[department_id]

# Ghi dữ liệu đã cập nhật xuống file CSV
fieldnames = ['BRANCH_ID', 'BRANCH_PHONE', 'BRANCH_NAME', 'BRANCH_ADDRESS', 'OPEN_TIME',
              'CLOSE_TIME', 'CAR_PARK', 'MOTORBIKE_PARK', 'MANAGER_ID', 'AREA_NAME']
write_csv(restaurant_branch_file, restaurant_branch_data, fieldnames)

print("Cập nhật manager_id và ghi file thành công!")