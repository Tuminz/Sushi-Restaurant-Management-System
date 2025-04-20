import csv
import random
from faker import Faker

# Khởi tạo đối tượng Faker
fake = Faker('vi_VN')

# Danh sách các món ăn theo từng thể loại
categories = {
    "Khai vị": ["Trứng hấp", "Súp miso", "Súp chay", "Trứng cá hồi", "Salad rong biển", 
                 "Edamame luộc", "Kimbap", "Gỏi cá hồi", "Gỏi cá ngừ", "Salad trái cây", 
                 "Đậu phụ chiên giòn", "Cá viên chiên", "Tôm chiên tempura", "Khoai tây chiên", 
                 "Nấm nướng", "Nem cuốn hải sản", "Gỏi cuốn tôm thịt", "Gỏi gà xé phay", 
                 "Súp kim chi", "Súp hải sản", "Sùng sùng rang muối", "Ốc hương nướng mỡ hành", 
                 "Bạch tuộc luộc", "Mực nướng sa tế", "Salad Nga", "Salad trái cây trộn sữa chua", 
                 "Chả giò hải sản", "Bánh bao chiên", "Bánh xèo hải sản"],
    "Sashimi combo": ["Sashimi tổng hợp", "Sashimi cá hồi đặc biệt", "Sashimi cá ngừ", "Sashimi cá trích", 
                      "Sashimi cá thu", "Sashimi mực", "Sashimi bạch tuộc", "Sashimi tôm", "Sashimi sò điệp", 
                      "Sashimi hàu", "Sashimi cá kiếm", "Sashimi cá ngựa", "Sashimi cá hồi áp chảo", 
                      "Sashimi cá ngừ sốt teriyaki", "Sashimi cá trích sốt ponzu", "Sashimi cá thu nướng muối", 
                      "Sashimi mực nướng sa tế", "Sashimi bạch tuộc luộc", "Sashimi tôm sốt mayonnaise", 
                      "Sashimi sò điệp nướng phô mai", "Sashimi hàu nướng mỡ hành", "Sashimi cá kiếm sốt bơ tỏi", 
                      "Sashimi cá ngựa hấp", "Sashimi cá hồi sốt cam", "Sashimi cá ngừ sốt tiêu đen", 
                      "Sashimi cá trích sốt wasabi", "Sashimi cá thu sốt ponzu", "Sashimi mực nướng muối ớt"],
    "Nigiri": ["Cá ngừ (2 miếng)", "Cá hồi (2 miếng)", "Lươn cá hồi nướng sốt (2 miếng)", "Cá trích", 
               "Cá thu", "Mực", "Bạch tuộc", "Tôm", "Sò điệp", "Hàu", "Cá kiếm", "Cá ngựa", 
               "Trứng cá", "Trứng cuộn", "Cá hồi áp chảo", "Cá ngừ sốt teriyaki", "Cá trích sốt ponzu", 
               "Cá thu nướng muối", "Mực nướng sa tế", "Bạch tuộc luộc", "Tôm sốt mayonnaise", 
               "Sò điệp nướng phô mai", "Hàu nướng mỡ hành", "Cá kiếm sốt bơ tỏi", "Cá ngựa hấp", 
               "Cá hồi sốt cam", "Cá ngừ sốt tiêu đen", "Cá trích sốt wasabi", "Cá thu sốt ponzu", 
               "Mực nướng muối ớt"],
    "Tempura": ["Tempura tôm", "Tempura rau", "Tempura mực", "Tempura bạch tuộc", "Tempura cá", 
                "Tempura khoai lang", "Tempura bí đỏ", "Tempura cà tím", "Tempura hành tây", "Tempura nấm", 
                "Tempura đậu hũ", "Tempura trái cây", "Tempura hải sản thập cẩm", "Tempura rau củ thập cẩm", 
                "Tempura kim châm", "Tempura đậu bắp", "Tempura súp lơ", "Tempura cà rốt", "Tempura ớt chuông", 
                "Tempura đậu que", "Tempura măng tây", "Tempura nấm kim châm", "Tempura tôm sú", "Tempura cá hồi", 
                "Tempura cá ngừ", "Tempura bạch tuộc sốt mayonnaise", "Tempura tôm sốt tartar", 
                "Tempura rau củ sốt mè rang"],
    "Udon": ["Udon xào", "Udon canh", "Udon hải sản", "Udon thịt bò", "Udon gà", "Udon chay", "Udon xào giòn", 
             "Udon xào cay", "Udon xào kim chi", "Udon xào bò lúc lắc", "Udon xào hải sản thập cẩm", 
             "Udon xào rau củ thập cẩm", "Udon xào nấm", "Udon xào hải sản sốt cay", "Udon xào bò sốt tiêu đen", 
             "Udon xào gà sốt teriyaki", "Udon xào chay sốt nấm", "Udon xào hải sản sốt chua ngọt", 
             "Udon xào bò sốt tiêu xanh", "Udon xào gà sốt me", "Udon xào rau củ sốt cà ri", 
             "Udon xào hải sản sốt bơ tỏi", "Udon xào bò sốt tiêu xanh", "Udon xào gà sốt satế", "Udon xào rau củ sốt nấm"],
    "Hotpot": ["Hotpot hải sản", "Hotpot thịt bò", "Hotpot thập cẩm", "Hotpot nấm", "Hotpot lẩu thái", 
               "Hotpot lẩu chua cay", "Hotpot lẩu xí quách", "Hotpot lẩu mắm", "Hotpot lẩu riêu cua", 
               "Hotpot lẩu nấm", "Hotpot lẩu kim chi", "Hotpot lẩu măng chua", "Hotpot lẩu xí quách hải sản", 
               "Hotpot lẩu chua cay hải sản", "Hotpot lẩu mắm hải sản", "Hotpot lẩu riêu cua hải sản", 
               "Hotpot lẩu nấm hải sản", "Hotpot lẩu kim chi hải sản", "Hotpot lẩu măng chua hải sản"],
    "Lunch set": ["Lunch set 1", "Lunch set 2", "Lunch set 3", "Lunch set 4", "Lunch set 5", "Lunch set 6", 
                  "Lunch set 7", "Lunch set 8", "Lunch set 9", "Lunch set 10"],
    "Các món nước": ["Nước cam", "Nước trà xanh", "Sinh tố dừa", "Nước ép bưởi", "Nước ép táo", 
                      "Nước ép dưa hấu", "Nước ép cà rốt", "Nước ép trái cây tổng hợp", "Nước ép rau má", 
                      "Nước dừa tươi", "Sinh tố bơ", "Sinh tố xoài", "Sinh tố chuối", "Sinh tố dâu", 
                      "Sinh tố việt quất", "Sinh tố kiwi", "Sinh tố táo xanh", "Sinh tố dưa lưới", 
                      "Sinh tố cà phê", "Sinh tố trà xanh", "Nước ép ổi", "Nước ép lê", "Nước ép cherry", 
                      "Trà đào", "Trà vải", "Trà tắc", "Trà chanh", "Soda chanh", "Soda cam", "Soda dâu"]
}

# Hàm tạo dữ liệu ngẫu nhiên
def generate_dish_data(dish_id, category, dish_name):
    # Lựa chọn giá ngẫu nhiên cho từng thể loại
    category_prices = {
        "Khai vị": (35000, 100000),
        "Sashimi combo": (150000, 500000),
        "Nigiri": (70000, 150000),
        "Tempura": (70000, 100000),
        "Udon": (50000, 100000),
        "Hotpot": (200000, 400000),
        "Lunch set": (300000, 500000),
        "Các món nước": (20000, 40000)
    }
    
    price_min, price_max = category_prices[category]
    dish_price = round(random.uniform(price_min, price_max), 2)
    
    return {
        "DISH_ID": f"D{dish_id:03d}",
        "DISH_NAME": dish_name,
        "CATEGORY": category,
        "PRICE": dish_price
    }

# Danh sách tất cả món ăn
all_dishes = []

# Tạo dữ liệu món ăn cho từng thể loại
dish_id = 1
for category, dishes in categories.items():
    for dish_name in dishes:
        all_dishes.append(generate_dish_data(dish_id, category, dish_name))
        dish_id += 1

# Ghi dữ liệu vào file CSV
with open('dish_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["DISH_ID", "DISH_NAME", "CATEGORY", "PRICE"])
    writer.writeheader()
    writer.writerows(all_dishes)

print("Đã tạo file menu.csv thành công!")
