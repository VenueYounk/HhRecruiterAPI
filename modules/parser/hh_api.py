import requests
import os
from dotenv import load_dotenv

load_dotenv()

MAX_RETRIES = 3  # Максимальное количество попыток
INDUSTRIES = requests.get("https://api.hh.ru/industries").json()


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
            self.access_token = self.response["access_token"]
            with open("./modules/parser/access_token.txt", "w") as file:
                file.write(self.access_token)
        else:
            print("Ошибка при получении access token:", self.response.text)
            return None

    def get_vacancies_from_employers(self, area=40, deep=49):
        self.result = []
        headers = {"Authorization": "Bearer " + self.access_token}
        for page in range(deep):
            retries = 0
            while retries < MAX_RETRIES:
                try:
                    print("Страница", page)
                    params = {
                        "area": area,
                        "type": "company",
                        "only_with_vacancies": True,
                        "per_page": 100,
                        "page": page,
                    }
                    employers = requests.get(
                        "https://api.hh.ru/employers", params=params, headers=headers
                    )
                    employers.raise_for_status()
                    employers_data = employers.json()
                    for employer in employers_data["items"]:
                        print("Получили работодателя", employer["name"])
                        info_employer = requests.get(
                            f"https://api.hh.ru/employers/{employer['id']}",
                            headers=headers,
                        ).json()
                        industries = ", ".join(
                            [
                                industry["name"]
                                for industry in info_employer["industries"]
                            ]
                        )
                        employer_data = {
                            "company_name": info_employer["name"],
                            "industry": industries,
                            "vacancies": [],
                        }
                        vacancy_params = {
                            "employer_id": employer["id"],
                            "per_page": 100,
                        }
                        vacancies = requests.get(
                            f"https://api.hh.ru/vacancies/",
                            params=vacancy_params,
                            headers=headers,
                        ).json()
                        for vacancy in vacancies["items"]:
                            if (
                                vacancy["contacts"] is not None
                                and vacancy["contacts"]["phones"]
                            ):
                                formatted = ",".join(
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
                        if employer_data["vacancies"]:
                            self.result.append(employer_data)
                    break
                except requests.exceptions.RequestException as e:
                    print("Ошибка при получении списка работодателей:", str(e))
                    retries += 1
            else:
                print("Превышено максимальное количество попыток.")
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
                                    "company_name": employer["name"],
                                    "industry": industries,
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
