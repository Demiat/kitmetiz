import json

with open(r'D:\Dev\kitmetiz\kitm\core\123.json', 'r', encoding='utf-8') as file:
    parsed_data = json.load(file)

# Обходим структуру
for uid in parsed_data:
    product_info = parsed_data[uid]
    print(f"Уникальный идентификатор: {uid}")
    print(f"Наименование: {product_info[0]}")
    print(f"Количество: {product_info[1]}")
    print(f"Цена: {product_info[2]}")
    print(f"Артикул: {product_info[3]}")
    print(f"Единица измерения: {product_info[4]}")
    print(f"Категория: {product_info[5]}\n")
