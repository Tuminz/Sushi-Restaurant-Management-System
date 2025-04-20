
'''
from faker import Faker
from datetime import date, timedelta
import csv
import random

# Khởi tạo Faker với ngôn ngữ tiếng Việt
fake = Faker('vi_VN')

# Đọc department_id từ file department_data.csv
def read_department_ids():
    department_data = []
    with open('department_data.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            department_data.append(row)
    return department_data

# Tạo dữ liệu employee
def generate_employee_data(department_data, num_employees=15000):
    employees = []
    department_salaries = {}
    current_date = date.today()  # Lấy ngày hiện tại

    # Gán salary cho các department
    for department in department_data:
        department_id = department['DEPARTMENT_ID']
        department_name = department['DEPARTMENT_NAME']

        if department_name == 'Quản lý chi nhánh':
            department_salaries[department_id] = 40000000  # Lương lớn nhất 40 triệu
        else:
            department_salaries[department_id] = random.randint(10000000, 40000000)

    # Phân loại bộ phận "Quản lý chi nhánh"
    branch_departments = [d for d in department_data if d['DEPARTMENT_NAME'] == 'Quản lý chi nhánh']
    branch_employees = []

    # Tạo dữ liệu cho bộ phận "Quản lý chi nhánh"
    for branch in branch_departments:
        employee_id = f"E{len(branch_employees) + 1:06d}"
        full_name = fake.name()
        dob = fake.date_of_birth(minimum_age=18, maximum_age=45)
        start_date = dob + timedelta(days=18 * 365)  # Ngày bắt đầu làm việc từ khi đủ 18 tuổi

        branch_employee = {
            'EMPLOYEE_ID': employee_id,
            'FULL_NAME': full_name,
            'DATE_OF_BIRTH': dob.strftime('%Y-%m-%d'),
            'GENDER': random.choice(["Nam", "Nữ"]),
            'SALARY': department_salaries[branch['DEPARTMENT_ID']],
            'START_DATE_WORK': start_date.strftime('%Y-%m-%d'),
            'TERMINATION_DATE': '',  # Bắt buộc trống
            'DEPARTMENT_ID': branch['DEPARTMENT_ID']
        }
        branch_employees.append(branch_employee)

    # Xác định ngày nhỏ nhất trong "Quản lý chi nhánh"
    global_min_start_date = min(
        date.fromisoformat(emp['START_DATE_WORK']) for emp in branch_employees
    )

    # Thêm dữ liệu của quản lý chi nhánh vào danh sách nhân viên
    employees.extend(branch_employees)

    # Tạo dữ liệu cho các nhân viên khác
    for i in range(len(branch_employees) + 1, num_employees + 1):
        employee_id = f"E{i:06d}"
        full_name = fake.name()
        dob = fake.date_of_birth(minimum_age=18, maximum_age=45)

        # Ngày bắt đầu làm việc phải sau ngày của "Quản lý chi nhánh"
        start_date = dob + timedelta(days=18 * 365)
        if start_date <= global_min_start_date:
            start_date = global_min_start_date + timedelta(days=random.randint(1, 365))

        # Xác định ngày nghỉ việc (nếu có)
        termination_date = None
        if random.random() > 0.6:  # 40% có giá trị
            termination_date = start_date + timedelta(days=random.randint(1, (45 - 18) * 365))
            if (termination_date - dob).days > 45 * 365 or termination_date >= current_date:
                termination_date = None

        # Gán department_id
        department = random.choice(department_data)
        while department['DEPARTMENT_NAME'] == 'Quản lý chi nhánh':
            department = random.choice(department_data)

        department_id = department['DEPARTMENT_ID']
        salary = department_salaries[department_id]
        gender = random.choice(["Nam", "Nữ"])

        employee = {
            'EMPLOYEE_ID': employee_id,
            'FULL_NAME': full_name,
            'DATE_OF_BIRTH': dob.strftime('%Y-%m-%d'),
            'GENDER': gender,
            'SALARY': salary,
            'START_DATE_WORK': start_date.strftime('%Y-%m-%d'),
            'TERMINATION_DATE': termination_date.strftime('%Y-%m-%d') if termination_date else '',
            'DEPARTMENT_ID': department_id
        }
        employees.append(employee)

    return employees

# Ghi dữ liệu employee ra file CSV
def write_employee_csv(employees, filename='employee_data.csv'):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'EMPLOYEE_ID', 'FULL_NAME', 'DATE_OF_BIRTH', 'GENDER', 'SALARY',
            'START_DATE_WORK', 'TERMINATION_DATE', 'DEPARTMENT_ID'
        ])
        writer.writeheader()
        writer.writerows(employees)

if __name__ == "__main__":
    department_data = read_department_ids()
    employees = generate_employee_data(department_data)
    write_employee_csv(employees)
    print("File employee_data.csv đã được tạo thành công!")
'''
from faker import Faker
from datetime import date, timedelta
import csv
import random

# Khởi tạo Faker với ngôn ngữ tiếng Việt
fake = Faker('vi_VN')

# Đọc department_id từ file department_data.csv
def read_department_ids():
    department_data = []
    with open('department_data.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            department_data.append(row)
    return department_data

# Tạo dữ liệu employee
def generate_employee_data(department_data, num_employees=15000):
    employees = []
    department_salaries = {}
    current_date = date.today()  # Lấy ngày hiện tại

    # Gán salary cho các department
    for department in department_data:
        department_id = department['DEPARTMENT_ID']
        department_name = department['DEPARTMENT_NAME']

        if department_name == 'Quản lý chi nhánh':
            department_salaries[department_id] = 40000000  # Lương lớn nhất 40 triệu
        else:
            department_salaries[department_id] = random.randint(10000000, 40000000)

    # Phân loại bộ phận "Quản lý chi nhánh"
    branch_departments = [d for d in department_data if d['DEPARTMENT_NAME'] == 'Quản lý chi nhánh']
    other_departments = [d for d in department_data if d['DEPARTMENT_NAME'] != 'Quản lý chi nhánh']

    # Tạo dữ liệu cho bộ phận "Quản lý chi nhánh"
    for branch in branch_departments:
        employee_id = f"E{len(employees) + 1:06d}"
        full_name = fake.name()
        dob = fake.date_of_birth(minimum_age=18, maximum_age=45)
        start_date = dob + timedelta(days=18 * 365)  # Ngày bắt đầu làm việc từ khi đủ 18 tuổi

        branch_employee = {
            'EMPLOYEE_ID': employee_id,
            'FULL_NAME': full_name,
            'DATE_OF_BIRTH': dob.strftime('%Y-%m-%d'),
            'GENDER': random.choice(["Nam", "Nữ"]),
            'SALARY': department_salaries[branch['DEPARTMENT_ID']],
            'START_DATE_WORK': start_date.strftime('%Y-%m-%d'),
            'TERMINATION_DATE': '',  # Bắt buộc trống
            'DEPARTMENT_ID': branch['DEPARTMENT_ID']
        }
        employees.append(branch_employee)

    # Xác định ngày nhỏ nhất trong "Quản lý chi nhánh"
    global_min_start_date = min(
        date.fromisoformat(emp['START_DATE_WORK']) for emp in employees
    )

    # Tạo dữ liệu cho các nhân viên khác
    for department in other_departments:
        department_id = department['DEPARTMENT_ID']

        # Đảm bảo mỗi phòng ban có ít nhất 2 nhân viên
        for _ in range(2):
            employee_id = f"E{len(employees) + 1:06d}"
            full_name = fake.name()
            dob = fake.date_of_birth(minimum_age=18, maximum_age=45)
            start_date = dob + timedelta(days=18 * 365)

            # Ngày bắt đầu làm việc phải sau ngày của "Quản lý chi nhánh"
            if start_date <= global_min_start_date:
                start_date = global_min_start_date + timedelta(days=random.randint(1, 365))

            termination_date = None
            if random.random() > 0.6:  # 40% có giá trị
                termination_date = start_date + timedelta(days=random.randint(1, (45 - 18) * 365))
                if (termination_date - dob).days > 45 * 365 or termination_date >= current_date:
                    termination_date = None

            employee = {
                'EMPLOYEE_ID': employee_id,
                'FULL_NAME': full_name,
                'DATE_OF_BIRTH': dob.strftime('%Y-%m-%d'),
                'GENDER': random.choice(["Nam", "Nữ"]),
                'SALARY': department_salaries[department_id],
                'START_DATE_WORK': start_date.strftime('%Y-%m-%d'),
                'TERMINATION_DATE': termination_date.strftime('%Y-%m-%d') if termination_date else '',
                'DEPARTMENT_ID': department_id
            }
            employees.append(employee)

        # Tạo thêm nhân viên ngẫu nhiên cho các phòng ban
        num_extra_employees = random.randint(0, max(0, num_employees - len(employees)))
        for _ in range(num_extra_employees):
            employee_id = f"E{len(employees) + 1:06d}"
            full_name = fake.name()
            dob = fake.date_of_birth(minimum_age=18, maximum_age=45)
            start_date = dob + timedelta(days=18 * 365)

            if start_date <= global_min_start_date:
                start_date = global_min_start_date + timedelta(days=random.randint(1, 365))

            termination_date = None
            if random.random() > 0.6:
                termination_date = start_date + timedelta(days=random.randint(1, (45 - 18) * 365))
                if (termination_date - dob).days > 45 * 365 or termination_date >= current_date:
                    termination_date = None

            employee = {
                'EMPLOYEE_ID': employee_id,
                'FULL_NAME': full_name,
                'DATE_OF_BIRTH': dob.strftime('%Y-%m-%d'),
                'GENDER': random.choice(["Nam", "Nữ"]),
                'SALARY': department_salaries[department_id],
                'START_DATE_WORK': start_date.strftime('%Y-%m-%d'),
                'TERMINATION_DATE': termination_date.strftime('%Y-%m-%d') if termination_date else '',
                'DEPARTMENT_ID': department_id
            }
            employees.append(employee)

    return employees

# Ghi dữ liệu employee ra file CSV
def write_employee_csv(employees, filename='employee_data.csv'):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'EMPLOYEE_ID', 'FULL_NAME', 'DATE_OF_BIRTH', 'GENDER', 'SALARY',
            'START_DATE_WORK', 'TERMINATION_DATE', 'DEPARTMENT_ID'
        ])
        writer.writeheader()
        writer.writerows(employees)

if __name__ == "__main__":
    department_data = read_department_ids()
    employees = generate_employee_data(department_data)
    write_employee_csv(employees)
    print("File employee_data.csv đã được tạo thành công!")
