import requests
import os
from dotenv import load_dotenv


load_dotenv()


INDUSTRIES = requests.get("https://api.hh.ru/industries").json()


# Context from Class or Interface c:/Users/Venue/Documents/python/FlaskApiHH/.venv/Lib/site-packages/pip/_internal/index/collector.py:LinkCollector


class HHAPI:
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")

    def __init__(self) -> None:
        with open("./modules/parser/access_token.txt", "r") as file:
            self.access_token = file.readline().strip()
        self.get_access_token()

    def get_access_token(self):
        self.response = requests.post(
            "https://hh.ru/oauth/token",
            data={
                "grant_type": "client_credentials",
                "client_id": self.CLIENT_ID,
                "client_secret": self.CLIENT_SECRET,
            },
        )
        if self.response.status_code == 200:
            self.response = self.response.json()
            # self.expires_in = self.response["expires_in"]
            # Парсим ответ и извлекаем access token

            self.access_token = self.response["access_token"]
            with open("./modules/parser/access_token.txt", "w") as file:
                file.write(self.access_token)
        else:
            # Обработка ошибки при получении access token
            print("Ошибка при получении access token:", self.response.text)
            return None

    def get_vacancies_from_employers(self, area=40, deep=49):
        self.result = []
        # page = 49
        headers = {"Authorization": "Bearer " + self.access_token}
        for page in range(deep):
            print("Страница ", page)
            params = {
                "area": area,
                "type": "company",
                "only_with_vacancies": True,
                "per_page": 100,
                "page": page,
            }

            # Получили список работодателей

            employers = requests.get(
                "https://api.hh.ru/employers", params=params, headers=headers
            )

            # Итерируемся по работодателям
            for employer in employers.json()["items"]:
                print("Получили работодателя ", employer["name"])
                # Получили информацию о работодателе
                info_employer = requests.get(
                    f"https://api.hh.ru/employers/{employer['id']}", headers=headers
                ).json()
                # Узнали его отрасль
                industries = ", ".join(
                    [industry["name"] for industry in info_employer["industries"]]
                )

                employer_data = {
                    "name": info_employer["name"],
                    "industries": industries,
                    "vacancies": [],
                }

                vacancy_params = {
                    "employer_id": employer["id"],
                    "per_page": 100,
                }
                # Получаем его вакансии
                vacancies = requests.get(
                    f"https://api.hh.ru/vacancies/?employer_id={employer['id']}",
                    headers=headers,
                ).json()
                # Итерируемся по вакансиям
                for vacancy in vacancies["items"]:
                    if vacancy["contacts"] is not None:
                        if (
                            vacancy["contacts"]["phones"] is not None
                            and len(vacancy["contacts"]["phones"]) > 0
                        ):
                            # print(vacancy["contacts"]["phones"]):
                            formatted = ", ".join(
                                [
                                    phone["formatted"]
                                    for phone in vacancy["contacts"]["phones"]
                                ]
                            )
                            employer_data["vacancies"].append(
                                {
                                    "name": vacancy["name"],
                                    "contact_name": vacancy["contacts"]["name"],
                                    "phone": formatted,
                                    "url": vacancy["alternate_url"],
                                }
                            )
                            # print(f"{vacancy['contacts']['name']} : {formatted}")
                if employer_data["vacancies"]:
                    self.result.append(employer_data)
        return self.result

    def get_employers_by_vacancy(self, area=40, deep=15):
        self.result = []
        for industry in INDUSTRIES:
            self.vacancies_with_phone = []

            # Задаем параметры фильтрации и сортировки
            for page in range(deep):
                print(industry["name"], page)
                params = {
                    "area": [
                        40,
                    ],
                    "industry": industry["id"],
                    "order_by": "publication_time",
                    "page": page,
                    "per_page": 100,
                }

                headers = {"Authorization": "Bearer " + self.access_token}

                response = requests.get(
                    "https://api.hh.ru/vacancies", params=params, headers=headers
                )
                if response.status_code == 200:
                    vacancies = response.json()
                    for vacancy in vacancies["items"]:
                        if (
                            vacancy["contacts"] is not None
                            and vacancy["contacts"]["phones"]
                        ):
                            formatted = ", ".join(
                                [
                                    phone["formatted"]
                                    for phone in vacancy["contacts"]["phones"]
                                ]
                            )

                            employer = requests.get(vacancy["employer"]["url"]).json()
                            industries = ", ".join(
                                [
                                    industry["name"]
                                    for industry in employer["industries"]
                                ]
                            )
                            self.result.append(
                                {
                                    "name": employer["name"],
                                    "industries": industries,
                                    "vacancies": [
                                        {
                                            "name": vacancy["name"],
                                            "contact_name": vacancy["contacts"]["name"],
                                            "phone": formatted,
                                            "url": vacancy["alternate_url"],
                                        }
                                    ],
                                }
                            )

                else:
                    print("Ошибка при получении списка вакансий:", response.text)
                    return None
        return self.result
