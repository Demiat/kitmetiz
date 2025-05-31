import requests


url = 'http://localhost/kit/hs/Products/get_prod?sklad=Основной склад'
response = requests.get(
    url,
    auth=(
        'Администратор'.encode('utf-8'),
        'евмут1982'.encode('utf-8')
    )
)
if response.status_code == 200:
    print(response.json())
    print("Запрос успешен!")
else:
    print(f'Ошибка {response.status_code}: {response.text}')

# import certifi
# print(certifi.where())
