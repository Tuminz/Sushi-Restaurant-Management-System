import csv
import random

# Đọc dữ liệu từ file CSV restaurant_branch_data.csv
def read_restaurant_branch_data():
    branches = []
    with open('restaurant_branch_data.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            branches.append(row['BRANCH_ID'])  # Chỉ lấy BRANCH_ID
    return branches

# Đọc dữ liệu từ file CSV dish_data.csv
def read_dish_data():
    dishes = []
    with open('dish_data.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dishes.append(row['DISH_ID'])  # Chỉ lấy DISH_ID
    return dishes

# Tạo dữ liệu cho bảng DISH_AVAILABLE
def create_dish_available_data(branches, dishes):
    data = []
    for branch_id in branches:
        for dish_id in dishes:
            # Tạo giá trị ngẫu nhiên cho IS_AVAILABLE và IS_DELIVERABLE
            is_available = random.choices([1, 0], weights=[90, 10])[0]
            is_deliverable = random.choices([1, 0], weights=[90, 10])[0]
            
            data.append({
                'BRANCH_ID': branch_id,
                'DISH_ID': dish_id,
                'IS_AVAILABLE': is_available,
                'IS_DELIVERABLE': is_deliverable
            })
    return data

# Ghi dữ liệu vào file CSV
def write_to_csv(data):
    with open('dish_available_data.csv', mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['BRANCH_ID', 'DISH_ID', 'IS_AVAILABLE', 'IS_DELIVERABLE']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Main
def main():
    branches = read_restaurant_branch_data()  # Đọc dữ liệu từ file restaurant_branch_data.csv
    dishes = read_dish_data()  # Đọc dữ liệu từ file dish_data.csv
    dish_available_data = create_dish_available_data(branches, dishes)  # Tạo dữ liệu cho bảng DISH_AVAILABLE
    write_to_csv(dish_available_data)  # Ghi dữ liệu xuống file dish_available_data.csv

if __name__ == '__main__':
    main()
