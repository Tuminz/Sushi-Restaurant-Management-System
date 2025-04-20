import csv
import random
from faker import Faker

# Khởi tạo đối tượng Faker để tạo tên tiếng Việt
fake = Faker('vi_VN')

# Mở file CSV để ghi
with open('customer_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Viết tiêu đề cho file CSV
    writer.writerow(['CUSTOMER_ID', 'FULL_NAME', 'PHONE_NUMBER', 'EMAIL', 'IDENTITY_CARD', 'GENDER'])

    # Tạo dữ liệu cho 100000 bản ghi
    for i in range(1, 100001):
        # customer_id: 000001C, 000002C, ..., 100000C
        customer_id = f'{i:06}C'  # Sử dụng 6 chữ số, sau đó thêm chữ "C"
        
        # full_name: tạo tên tiếng Việt
        full_name = fake.name()
        
        # phone_number: tạo số điện thoại không trùng nhau
        phone_number = f'0{random.randint(100000000, 999999999)}'
        
        # email: tạo email có đuôi @gmail.com, tên email là chữ cái và chữ số, tối đa 10 ký tự
        email_name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))
        email = f'{email_name}@gmail.com'
        
        # identity_card: tạo số chứng minh nhân dân không trùng nhau
        identity_card = f'{random.randint(100000000, 999999999)}'
        
        # gender: ngẫu nhiên giới tính Nam hoặc Nữ
        gender = random.choice(['Nam', 'Nữ'])
        
        # Ghi dữ liệu vào file CSV
        writer.writerow([customer_id, full_name, phone_number, email, identity_card, gender])

print("Dữ liệu đã được tạo và lưu vào customer_data.csv thành công!")
