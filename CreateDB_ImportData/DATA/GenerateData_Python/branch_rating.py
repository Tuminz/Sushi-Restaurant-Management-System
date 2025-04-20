
'''
import csv
import random
from faker import Faker

def generate_branch_rating_data(invoice_file, order_file, output_file):
    # Khởi tạo faker
    fake = Faker()
    
    # Đọc dữ liệu từ invoice_data.csv
    invoice_data = {}
    with open(invoice_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            invoice_data[row['INVOICE_ID']] = {
                'ORDER_ID': row['ORDER_ID'],
                'ISSUE_DATE': row['ISSUE_DATE']
            }

    # Đọc dữ liệu từ order_data.csv
    order_data = {}
    with open(order_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            order_data[row['ORDER_ID']] = row['BRANCH_ID']

    # Tạo dữ liệu cho BRANCH_RATING
    data = []
    for i in range(1, 101001):
        rating_id = f"R{i:06d}"

        # Tạo rating values theo xác suất 80%-20%
        ratings = [
            random.choices([5] * 4 + [1, 2, 3, 4], k=1)[0] for _ in range(5)
        ]
        
        # Tạo comment theo yêu cầu
        if all(r == 5 for r in ratings):
            comments = "TẤT CẢ ĐỀU TỐT VÀ KHÔNG CÓ GÌ ĐỂ CHÊ."
        elif any(r in [1, 2] for r in ratings):
            comments = "QUÁN CÒN THIẾU SÓT CẦN CẢI THIỆN NHIỀU!"
        else:
            comments = "MỌI THỨ CỦA QUÁN ĐỀU ỔN."

        # Giới hạn độ dài của comment
        comments = comments[:200]

        # Chọn invoice_id ngẫu nhiên từ dữ liệu có sẵn
        invoice_id = random.choice(list(invoice_data.keys()))

        # Lấy thông tin order_id và branch_id
        order_id = invoice_data[invoice_id]['ORDER_ID']
        branch_id = order_data.get(order_id, None)

        # Lấy rating_date từ issue_date
        rating_date = invoice_data[invoice_id]['ISSUE_DATE']

        # Thêm vào danh sách dữ liệu
        data.append([
            rating_id,
            ratings[0], ratings[1], ratings[2], ratings[3], ratings[4],
            comments,
            branch_id,
            rating_date,
            invoice_id
        ])

    # Ghi dữ liệu xuống file CSV
    with open(output_file, mode='w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "RATING_ID", "SERVICE_RATING", "LOCATION_RATING", "PRICE_RATING", 
            "DISH_QUALITY_RATING", "ENVIRONMENT_RATING", "COMMENTS", "BRANCH_ID", 
            "RATING_DATE", "INVOICE_ID"
        ])
        writer.writerows(data)

# Sử dụng hàm để tạo dữ liệu
invoice_file = 'invoice_data.csv'
order_file = 'order_data.csv'
output_file = 'branch_rating_data.csv'
generate_branch_rating_data(invoice_file, order_file, output_file)
'''
import csv
import random
from faker import Faker
from datetime import datetime

def generate_branch_rating_data(invoice_file, order_file, output_file):
    # Khởi tạo faker
    fake = Faker()

    # Đọc dữ liệu từ invoice_data.csv
    invoice_data = {}
    with open(invoice_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            invoice_data[row['INVOICE_ID']] = {
                'ORDER_ID': row['ORDER_ID'],
                'ISSUE_DATE': row['ISSUE_DATE']
            }

    # Đọc dữ liệu từ order_data.csv
    order_data = {}
    with open(order_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            order_data[row['ORDER_ID']] = row['BRANCH_ID']

    # Tạo dữ liệu cho BRANCH_RATING
    data = []
    for i, invoice_id in enumerate(invoice_data.keys(), start=1):
        rating_id = f"R{i:06d}"

        # Tạo rating values theo xác suất 80%-20%
        ratings = [
            random.choices([5] * 8 + [1, 2, 3, 4], k=1)[0] for _ in range(5)
        ]

        # Tạo comment theo yêu cầu
        if all(r == 5 for r in ratings):
            comments = "TẤT CẢ ĐỀU TỐT VÀ KHÔNG CÓ GÌ ĐỂ CHÊ."
        elif any(r in [1, 2] for r in ratings):
            comments = "QUÁN CÒN THIẾU SÓT CẦN CẢI THIỆN NHIỀU!"
        else:
            comments = "MỌI THỨ CỦA QUÁN ĐỀU ỔN."

        # Giới hạn độ dài của comment
        comments = comments[:200]

        # Lấy thông tin order_id và branch_id
        order_id = invoice_data[invoice_id]['ORDER_ID']
        branch_id = order_data.get(order_id, None)

        # Lấy rating_date từ issue_date và chuyển thành định dạng DATE (YYYY-MM-DD)
        rating_date_str = invoice_data[invoice_id]['ISSUE_DATE']
        try:
            rating_date = datetime.strptime(rating_date_str, '%Y-%m-%d').date()
        except ValueError:
            # Nếu ngày không hợp lệ, gán giá trị mặc định (có thể điều chỉnh thêm)
            rating_date = datetime.today().date()

        # Thêm vào danh sách dữ liệu
        data.append([
            rating_id,
            ratings[0], ratings[1], ratings[2], ratings[3], ratings[4],
            comments,
            branch_id,
            rating_date,  # Sử dụng rating_date kiểu DATE
            invoice_id
        ])

    # Ghi dữ liệu xuống file CSV
    with open(output_file, mode='w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "RATING_ID", "SERVICE_RATING", "LOCATION_RATING", "PRICE_RATING", 
            "DISH_QUALITY_RATING", "ENVIRONMENT_RATING", "COMMENTS", "BRANCH_ID", 
            "RATING_DATE", "INVOICE_ID"
        ])
        writer.writerows(data)

# Sử dụng hàm để tạo dữ liệu
invoice_file = 'invoice_data.csv'
order_file = 'order_data.csv'
output_file = 'branch_rating_data.csv'
generate_branch_rating_data(invoice_file, order_file, output_file)

