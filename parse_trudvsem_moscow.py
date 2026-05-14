import requests
import json
from docx import Document

def get_vacancies():
    url = "https://opendata.trudvsem.ru/api/v1/vacancies"
    results = []
    seen_urls = set()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    # Try different search terms
    search_terms = ["учитель физической культуры", "преподаватель физической культуры", "учитель физкультуры"]

    for term in search_terms:
        for offset in range(20): # increased offset
            params = {
                "text": term,
                "region": "77", # Moscow
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
                    company = vacancy.get('company', {})
                    company_name = company.get('name', '')
                    vac_url = company.get('url', vacancy.get('vac_url', ''))

                    if vac_url in seen_urls:
                        continue

                    # Filter only Moscow public schools
                    is_school = 'ГБОУ' in company_name.upper() or 'ШКОЛА' in company_name.upper() or 'ОБЩЕОБРАЗОВАТЕЛЬНОЕ' in company_name.upper()

                    # Sometimes region 77 still returns other regions on Trudvsem, so check region string or address
                    region_name = vacancy.get('region', {}).get('name', '').upper()
                    address = vacancy.get('addresses', {}).get('address', [{}])[0].get('location', '').upper()

                    is_moscow = 'МОСКВА' in region_name or 'МОСКВА' in address or 'МОСКВЫ' in company_name.upper()

                    if is_school and is_moscow:
                        results.append({
                            'company': company_name,
                            'email': company.get('email', 'Не указан'),
                            'phone': company.get('phone', 'Не указан'),
                            'url': vac_url,
                            'title': vacancy.get('job-name', 'Учитель физической культуры')
                        })
                        seen_urls.add(vac_url)

                        if len(results) >= 20:
                            return results
            except Exception as e:
                print(f"Error on {term} offset {offset}: {e}")

    return results

vacancies = get_vacancies()
print(f"Found {len(vacancies)} vacancies")
if vacancies:
    print(json.dumps(vacancies, ensure_ascii=False, indent=2))
