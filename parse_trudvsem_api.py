import requests
import json

def get_vacancies():
    # Use the official Trudvsem Open Data API
    url = "https://opendata.trudvsem.ru/api/v1/vacancies"
    results = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    # Try different search terms
    search_terms = ["учитель физической культуры", "преподаватель физической культуры", "учитель физкультуры"]

    for term in search_terms:
        for offset in range(5):
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
                    company_name = vacancy.get('company', {}).get('name', '')

                    # Log some companies to debug

                    if 'ГБОУ' in company_name.upper() or 'ШКОЛА' in company_name.upper():
                        # Make sure it's not a duplicate
                        if not any(r['url'] == vacancy.get('vac_url') for r in results):
                            results.append({
                                'company': company_name,
                                'email': vacancy.get('company', {}).get('email', 'Не указан'),
                                'phone': vacancy.get('company', {}).get('phone', 'Не указан'),
                                'url': vacancy.get('company', {}).get('url', vacancy.get('vac_url', 'Не указан')),
                                'title': vacancy.get('job-name', 'Учитель физической культуры')
                            })

                            if len(results) >= 20:
                                return results
            except Exception as e:
                print(f"Error on {term} offset {offset}: {e}")

    return results

vacancies = get_vacancies()
print(f"Found {len(vacancies)} vacancies")
if vacancies:
    print(json.dumps(vacancies[:3], ensure_ascii=False, indent=2))
