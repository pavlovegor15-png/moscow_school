import requests
import json

def get_vacancies():
    url = "https://opendata.trudvsem.ru/api/v1/vacancies"
    results = []
    offset = 0

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    while len(results) < 20:
        params = {
            "text": "учитель физической культуры",
            "region": "77", # Moscow region code
            "offset": offset,
            "limit": 100
        }
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            if 'results' not in data or 'vacancies' not in data['results']:
                break

            for vac in data['results']['vacancies']:
                vacancy = vac['vacancy']
                company_name = vacancy.get('company', {}).get('name', '')

                # Check if it's a Moscow school
                if 'ГБОУ' in company_name.upper() and ('МОСКВ' in company_name.upper() or 'Г. МОСКВЫ' in company_name.upper() or 'ГОРОДА МОСКВЫ' in company_name.upper() or vacancy.get('region', {}).get('region_code') == '7700000000000'):
                    results.append({
                        'company': company_name,
                        'email': vacancy.get('company', {}).get('email', 'Не указан'),
                        'phone': vacancy.get('company', {}).get('phone', 'Не указан'),
                        'url': vacancy.get('company', {}).get('url', vacancy.get('vac_url', 'Не указан')),
                        'title': vacancy.get('job-name', 'Учитель физической культуры')
                    })
                    if len(results) >= 20:
                        break

            offset += 1
            if offset > 10: # limit to avoid infinite loop
                break
        except Exception as e:
            print(f"Error: {e}")
            break

    return results

print(json.dumps(get_vacancies(), ensure_ascii=False, indent=2))
