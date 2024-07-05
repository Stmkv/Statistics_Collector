import requests


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    if salary_from and not salary_to:
        return salary_from * 1.2
    if not salary_from and salary_to:
        return salary_to * 0.8
    return None


def get_number_vacancies(programming_languages):
    number_vacancies = {}
    url = "https://api.hh.ru/vacancies?"

    for language in programming_languages:
        params = {
            "professional_role": "96",
            "area": "1",
            "period": 30,
            "text": f"Программист {language}"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        response = response.json()
        number_vacancies[language] = response["found"]
    return number_vacancies


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
