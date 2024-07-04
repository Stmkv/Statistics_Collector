import requests
import pprint

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
    url = "https://api.hh.ru/vacancies?"
    params = {
            "professional_role": "96",
            "area": "1",
            "period": 30,
            "text": "Программист Python",
            "only_with_salary": True
        }
    response = requests.get(url, params=params)
    response.raise_for_status()
    response = response.json()
    for number in range(len(response["items"])):
        print(response["items"][number]["salary"])


if __name__ == "__main__":
    programming_languages = ["TypeScript", "Swift",
                            "Go", "C", "C#", "C++",
                            "Python", "Java", "JavaScript"
                            ]
    # pprint.pprint(get_number_vacancies(programming_languages))
    get_salary()
