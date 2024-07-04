import requests


url = "https://api.hh.ru/vacancies?"
params = {
    "professional_role": "96",
    "area": "1",
    "period": 30,
    "text": "python",
    "page": 1
}
response = requests.get(url, params=params)
response.raise_for_status()
x = response.json()
print(len(x['items']))
