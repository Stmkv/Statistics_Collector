import requests
import terminaltables
import os
from dotenv import load_dotenv


SJ_CATALOGUE_ID = 48
SJ_COUNT = 100
HH_PROFESSIONAL_ROLE_ID = 96
HH_AREA_ID = 1
HH_COUNT = 100
HH_PERIOD = 30


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
        "professional_role": HH_PROFESSIONAL_ROLE_ID,
        "area": HH_AREA_ID,
        "period": HH_PERIOD,
        "text": f"Программист {language}",
        "per_page": HH_COUNT
    }
    page = 0
    salaries = []
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


def get_sj_vacancies(language, key):
    url = "https://api.superjob.ru/2.0/vacancies/"
    params = {
        "keyword": f"Программист {language}",
        "town": "Москва",
        "catalogues": SJ_CATALOGUE_ID,
        "count": SJ_COUNT
    }
    page = 0
    salaries = []
    while True:
        params['page'] = page
        response = requests.get(url, headers={
            'X-Api-App-Id': key}, params=params)
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


def calculate_statistics(salaries, total_vacancies):
    if salaries:
        average_salary = round(sum(salaries) / len(salaries))
    else:
        average_salary = 0
    vacancies_processed = len(salaries)
    return {
        'vacancies_found': total_vacancies,
        'vacancies_processed': vacancies_processed,
        'average_salary': average_salary
    }


def print_table(statistics, title):
    table_data = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]

    for language, stats in statistics.items():
        table_data.append([
            language,
            stats['vacancies_found'],
            stats['vacancies_processed'],
            stats['average_salary']
        ])

    table_instance = terminaltables.AsciiTable(table_data, title=title)
    print(table_instance.table)


def main():
    load_dotenv()
    secret_ket = os.environ["SUPER_JOB_SECRET_KEY"]
    programming_languages = ["TypeScript", "Swift", "Go", "C", "C#", "C++", "Python", "Java"]

    sj_statistics = {}
    hh_statistics = {}

    for language in programming_languages:
        sj_salaries, sj_total_vacancies = get_sj_vacancies(language, secret_ket)
        sj_statistics[language] = calculate_statistics(sj_salaries, sj_total_vacancies)

        hh_salaries, hh_total_vacancies = get_hh_vacancies(language)
        hh_statistics[language] = calculate_statistics(hh_salaries, hh_total_vacancies)

    print_table(sj_statistics, title='SuperJob Moscow')
    print_table(hh_statistics, title='HeadHunter Moscow')


if __name__ == "__main__":
    main()
