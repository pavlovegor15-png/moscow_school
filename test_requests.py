import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Use msk.ru job sites or yandex rabota proxy
url = "https://api.hh.ru/vacancies"
params = {
    "text": "учитель физкультуры ГБОУ",
    "area": 1,
    "per_page": 100
}

try:
    response = requests.get(url, params=params, headers=headers)
    print(response.status_code)
except Exception as e:
    print(e)
