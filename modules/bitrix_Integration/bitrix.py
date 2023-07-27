import requests
import datetime
from dotenv import load_dotenv
import os
import time

load_dotenv()


BITRIX_CODE = os.getenv("BITRIX_CODE")
count = 1


today = datetime.datetime.now().date()


def add_bitrix_company(name: str, industry: str):
    """
    Adds a company to the Bitrix24 CRM.

    Parameters:
        name (str): The name of the company to be added.
        industry (str): The industry of the company to be added.

    Returns:
        int: The ID of the company.
    """
    response = requests.get(
        f"https://perfectstaff.bitrix24.kz/rest/1/{BITRIX_CODE}/crm.company.add.json?FIELDS[TITLE]={name}&FIELDS[INDUSTRY]={industry}"
    )
    try:
        return response.json()["result"]
    except Exception as e:
        time.sleep(60)
        return response.json()["result"]


def add_bitrix_contact(phone: str, name: str, company_bitrix_id: int):
    """
    Adds a contact to the Bitrix24 CRM.

    Returns:
    int: The ID of the company.
    """
    phones = phone.split(",")
    count = 0
    request_for_phone = ""
    for phone in phones:
        request_for_phone += f"&FIELDS[PHONE][{count}][VALUE]={phone}"
        count += 1
    response = requests.get(
        f"https://perfectstaff.bitrix24.kz/rest/1/{BITRIX_CODE}/crm.contact.add.json?FIELDS[NAME]={name}{request_for_phone}&FIELDS[COMPANY_ID]={company_bitrix_id}"
    )
    try:
        return response.json()["result"]
    except Exception as e:
        time.sleep(60)
        return response.json()["result"]


def update_bitrix_contact(bitrix_id, phone):
    phones = phone.split(",")
    count = 0
    request_for_phone = ""
    for phone in phones:
        request_for_phone += f"&FIELDS[PHONE][{count}][VALUE]={phone}"
        count += 1
    response = requests.get(
        f"https://perfectstaff.bitrix24.kz/rest/1/{BITRIX_CODE}/crm.contact.update.json?ID={bitrix_id}{request_for_phone}"
    )
    try:
        print(response.json())

        return response.json()["result"]
    except Exception as e:
        time.sleep(60)
        print(response.json())
        return response.json()["result"]


def add_bitrix_lead(
    vacancy_name: str,
    phone_bitrix_id: int,
    company_bitrix_id: int,
    url: str,
):
    response = requests.get(
        f"https://perfectstaff.bitrix24.kz/rest/1/{BITRIX_CODE}/crm.lead.add.json?FIELDS[TITLE]={vacancy_name}&FIELDS[WEB][0][VALUE]={url}&FIELDS[COMPANY_ID]={company_bitrix_id}&FIELDS[CONTACT_ID]={phone_bitrix_id}&FIELDS[SOURCE_DESCRIPTION]={url}"
    )
    try:
        return response.json()["result"]
    except Exception as e:
        time.sleep(60)
        return response.json()["result"]


# companies = requests.get(
#     f"http://85.198.90.82:8000/companies?sort_by=name&page={count}&results_per_page=5"
# ).json()

# print(companies[0])

# response = requests.get(
#     f"https://perfectstaff.bitrix24.kz/rest/1/{BITRIX_CODE}/crm.company.add.json?FIELDS[TITLE]=TESTCOMPANY"
# )
# # crm.company.list


# response = requests.get(
#     f"https://perfectstaff.bitrix24.kz/rest/1/2x828hyvmerd5824/crm.company.list.json?FIELDS[TITLE]=TESTCOMPANY"
# )
# print(response, response.json())

# count += 1
# if companies == []:
#     break
# for company in companies:
#     company_name = company["company_name"]
#     industry = company["industry"]
#     contact_phone = ""
#     url = ""
#     if len(company["vacancies"]) > 0:
#         contact_name = company["vacancies"][0]["contact_name"]
#         for vacancy in company["vacancies"]:
#             contact_phone += vacancy["phone"] + " "
#             url += vacancy["url"] + " "
#     print(company_name, industry, contact_name, contact_phone, url)
#     response = requests.get(
#         f"https://perfectstaff.bitrix24.kz/rest/1/2x828hyvmerd5824/crm.lead.add.json?FIELDS[TITLE]={company_name} {today}&FIELDS[NAME]={contact_name}&FIELDS[PHONE][0][VALUE]={contact_phone}&FIELDS[WEB][0][VALUE]={url}&FIELDS[SOURCE_DESCRIPTION]={industry}"
#     )
