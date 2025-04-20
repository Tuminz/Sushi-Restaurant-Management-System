import csv
import random
from faker import Faker

# Khởi tạo Faker
fake = Faker('vi_VN')

# Tên tỉnh/thành phố và số lần xuất hiện
cities = [
    ("Hà Nội", 3),
    ("Thành phố Hồ Chí Minh", 3),
    ("Đà Nẵng", 2),
    ("Nha Trang", 1),
    ("Bình Dương", 2),
    ("Cần Thơ", 1),
    ("Hải Phòng", 1),
    ("Huế", 1),
    ("Quảng Ninh", 1)
]

# Địa chỉ cụ thể theo tỉnh/thành phố
address_options = {
    "Hà Nội": ["Cầu Giấy - Hà Nội", "Hà Đông - Hà Nội", "Ba Đình - Hà Nội"],
    "Thành phố Hồ Chí Minh": [
        "Quận 1 - Thành phố Hồ Chí Minh",
        "Quận 3 - Thành phố Hồ Chí Minh",
        "Quận Bình Thạnh - Thành phố Hồ Chí Minh"
    ],
    "Hải Phòng": ["Dương Kinh - Hải Phòng"],
    "Đà Nẵng": ["Ngũ Hành Sơn - Đà Nẵng", "Sơn Trà - Đà Nẵng"],
    "Cần Thơ": ["Ô Môn - Cần Thơ"],
    "Huế": ["Kim Long - Huế"],
    "Bình Dương": ["Thuận An - Bình Dương", "Tân Uyên - Bình Dương"],
    "Nha Trang": ["Ninh Hòa - Nha Trang"],
    "Quảng Ninh": ["Đông Triều - Quảng Ninh"]
}

# Sinh danh sách branch_id
branch_ids = [f"B{i:03}" for i in range(1, 16)]

# Hàm tạo dữ liệu mở cửa và đóng cửa
def generate_open_close_time():
    open_hour = random.randint(6, 8)  # Giờ mở cửa từ 6h đến 8h sáng
    close_hour = open_hour + random.randint(13, 17)  # Đóng cửa từ 13 đến 17 giờ sau
    open_minute = random.choice([0, 30])
    close_minute = random.choice([0, 30])
    if close_hour > 23:  # Đảm bảo giờ đóng cửa không quá 23h
        close_hour = 23
        close_minute = 0
    return f"{open_hour:02}:{open_minute:02}:00", f"{close_hour:02}:{close_minute:02}:00"

# Phân bổ thành phố cho các branch_id
city_pool = [city for city, count in cities for _ in range(count)]
random.shuffle(city_pool)

# Sinh dữ liệu
data = []
used_address = {city: [] for city in address_options.keys()}
used_name_suffix = {city: 0 for city in address_options.keys()}

for i, branch_id in enumerate(branch_ids):
    area_name = city_pool[i]

    # Lấy địa chỉ không trùng
    address_list = address_options[area_name]
    branch_address = random.choice(
        [addr for addr in address_list if addr not in used_address[area_name]]
    )
    used_address[area_name].append(branch_address)

    # Tạo số điện thoại
    branch_phone = fake.phone_number()

    # Tạo tên nhà hàng với số thứ tự tăng dần
    used_name_suffix[area_name] += 1
    branch_name = f"Nhà hàng {area_name} {used_name_suffix[area_name]}"

    # Tạo giờ mở cửa và đóng cửa
    open_time, close_time = generate_open_close_time()

    # Tạo dữ liệu cho cột CAR_PARK và MOTORBIKE_PARK
    car_park = random.randint(0, 1)
    motorbike_park = random.randint(0, 1)

    # Thêm dữ liệu vào danh sách
    data.append([
        branch_id, branch_phone, branch_name, branch_address,
        open_time, close_time, car_park, motorbike_park, "", area_name
    ])

# Ghi dữ liệu ra file CSV
csv_file = "restaurant_branch_data.csv"
headers = [
    "BRANCH_ID", "BRANCH_PHONE", "BRANCH_NAME", "BRANCH_ADDRESS",
    "OPEN_TIME", "CLOSE_TIME", "CAR_PARK", "MOTORBIKE_PARK",
    "MANAGER_ID", "AREA_NAME"
]

with open(csv_file, mode="w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(data)

print(f"Dữ liệu đã được ghi vào file {csv_file}.")
