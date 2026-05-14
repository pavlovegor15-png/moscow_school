import requests
from bs4 import BeautifulSoup
import json
import re

def search_schools_yandex():
    url = "https://yandex.ru/search/xml"
    # using open yandex search xml might require credentials
    pass

def search_superjob():
    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        # 'X-Api-App-Id': 'your_secret_key' # requires auth
    }
    pass

print("Need a better approach")
