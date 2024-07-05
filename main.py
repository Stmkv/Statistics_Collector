import requests


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    if salary_from and not salary_to:
        return salary_from * 1.2
    if not salary_from and salary_to:
        return salary_to * 0.8
    return None


def predict_rub_salary_hh(vacancy):
    salary = vacancy.get('salary')
    if salary and salary['currency'] == 'RUR':
        return predict_salary(salary['from'], salary['to'])
    return None


def predict_rub_salary_sj(vacancy):
    salary_from = vacancy.get('payment_from')
    salary_to = vacancy.get('payment_to')
    return predict_salary(salary_from, salary_to)


def get_hh_vacancies(language):
    url = "https://api.hh.ru/vacancies"
    params = {
        "professional_role": 96,
        "area": 1,
        "period": 30,
        "text": f"Программист {language}",
        "per_page": 100
    }
    page = 0
    salaries = []
    total_vacancies = 0
    while True:
        params['page'] = page
        response = requests.get(url, headers={'User-Agent': 'api-test-agent'}, params=params)
        response.raise_for_status()
        response = response.json()
        total_vacancies = response['found']
        for item in response['items']:
            salary = predict_rub_salary_hh(item)
            if salary:
                salaries.append(salary)
        if page >= response['pages'] - 1:
            break
        page += 1
    return salaries, total_vacancies


def get_sj_vacancies(language):
    url = "https://api.superjob.ru/2.0/vacancies/"
    params = {
        "keyword": f"Программист {language}",
        "town": "Москва",
        "catalogues": 48,
        "count": 100
    }
    page = 0
    salaries = []
    total_vacancies = 0
    while True:
        params['page'] = page
        response = requests.get(url, headers={
    'X-Api-App-Id': 'v3.r.136975842.cce41f33febf1b5b393cffa55919bb5147188d2f.c98da888da9efe5721641c2d80223af0b5078f0e'}, params=params)
        response.raise_for_status()
        response = response.json()
        total_vacancies = response['total']
        for vacancy in response['objects']:
            salary = predict_rub_salary_sj(vacancy)
            if salary:
                salaries.append(salary)
        if not response['more']:
            break
        page += 1
    return salaries, total_vacancies


def get_salary():
    salaryes = []
    url = "https://api.hh.ru/vacancies?"
    params = {
            "professional_role": "96",
            "area": "1",
            "period": 30,
            "text": "Программист Python",
        }
    response = requests.get(url, params=params)
    response.raise_for_status()
    response = response.json()
    for number in range(len(response["items"])):
        salaryes.append(response["items"][number]["salary"])
    return salaryes


def predict_rub_salary(salaryes: list):
    predict_salary = []
    for salary in salaryes:
        if salary and salary["currency"] == 'RUR':
            if salary['from'] and salary["to"]:
                predict_salary.append((salary['from'] + salary["to"]) / 2)
            if salary['from'] and not salary["to"]:
                predict_salary.append(salary['from'] * 1.2)
            if not salary['from'] and salary["to"]:
                predict_salary.append(salary['to'] * 0.8)
        else:
            predict_salary.append(None)
    return predict_salary


if __name__ == "__main__":
    programming_languages = ["TypeScript", "Swift",
                            "Go", "C", "C#", "C++",
                            "Python", "Java", "JavaScript"
                            ]
    # pprint.pprint(get_number_vacancies(programming_languages))
    salaryes = get_salary()
    print(predict_rub_salary(salaryes))
