from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from modules.database.models import Company, Vacancy, Phones, session
from modules.bitrix_Integration.bitrix import (
    add_bitrix_company,
    add_bitrix_contact,
    add_bitrix_lead,
    update_bitrix_contact,
)
import datetime

# import logging

# logging.disable(logging.WARNING)

# Create a SQLite database engine and session


def drop_tables():
    # session.query(Company).delete()
    session.query(Vacancy).delete()
    session.commit()


# Function to add data to the database
# def add_data(data):
#     companies_added = 0
#     vacancies_added = 0

#     for comp in data:
#         company = session.query(Company).filter_by(name=comp["name"]).first()

#         if company is None:
#             company = Company(name=comp["name"], industries=comp["industries"])
#             session.add(company)
#             companies_added += 1

#         for vacancy_data in comp["vacancies"]:
#             vacancy = (
#                 session.query(Vacancy)
#                 .filter_by(name=vacancy_data["name"], company_id=company.id)
#                 .first()
#             )

#             if vacancy is None:
#                 vacancy = Vacancy(
#                     name=vacancy_data["name"],
#                     contact_name=vacancy_data["contact_name"],
#                     phone=vacancy_data["phone"],
#                     company_id=company.id,
#                     url=vacancy_data["url"],
#                 )
#                 company.vacancies.append(vacancy)
#                 session.add(vacancy)
#                 vacancies_added += 1

#     session.commit()

#     print(f"Companies added: {companies_added}")
#     print(f"Vacancies added: {vacancies_added}")


def save_phones():
    vacancies = session.query(Vacancy).all()
    phones_added = 0

    for vacancy in vacancies:
        company = vacancy.company
        contact_name = vacancy.contact_name
        phones = vacancy.phone.split(",")

        for phone in phones:
            print(phone)
            phone_data = (
                session.query(Phones)
                .filter_by(
                    phone=phone.strip(), company_id=company.id, name=contact_name
                )
                .first()
            )

            if phone_data is None:  # Corrected line
                phone_data = Phones(
                    phone=phone.strip(),
                    company_id=company.id,
                    name=contact_name,
                )
                session.add(phone_data)
                phones_added += 1

    session.commit()


def add_data(data):
    today = datetime.datetime.now().date()

    companies_added = 0
    vacancies_added = 0
    for comp in data:
        company = session.query(Company).filter_by(name=comp["company_name"]).first()

        if company is None:
            try:
                bitrix_company_id = add_bitrix_company(
                    comp["company_name"], comp["industry"]
                )
            except Exception as e:
                print("ОШИБКА С ДОБАВЛЕНИЕМ КОМПАНИИ В БИТРИКС", e)

                continue
            company = Company(
                name=comp["company_name"],
                industries=comp["industry"],
                bitrix_id=bitrix_company_id,
            )
            session.add(company)
            session.commit()

            companies_added += 1

        for vacancy_data in comp["vacancies"]:
            vacancy = (
                session.query(Vacancy)
                .filter_by(name=vacancy_data["name"], company_id=company.id)
                .first()
            )

            if vacancy is None:
                vacancy_data["phone"] = vacancy_data["phone"].replace(" ", "")
                phone = (
                    session.query(Phones)
                    .filter_by(name=vacancy_data["contact_name"], company_id=company.id)
                    .first()
                )

                if phone is None:
                    try:
                        bitrix_contact_id = add_bitrix_contact(
                            vacancy_data["phone"],
                            vacancy_data["contact_name"],
                            company.bitrix_id,
                        )
                    except Exception as e:
                        print("ОШИБКА С ДОБАВЛЕНИЕМ КОНТАКТА В БИТРИКС", e)
                        continue
                    phone = Phones(
                        phone=vacancy_data["phone"],
                        company_id=company.id,
                        name=vacancy_data["contact_name"],
                        bitrix_id=bitrix_contact_id,
                    )
                    session.add(phone)
                    session.commit()
                else:
                    phones = phone.phone.split(",")
                    vacancy_phones = vacancy_data["phone"].split(",")
                    for vacancy_phone in vacancy_phones:
                        if vacancy_phone not in phones:
                            phones.append(vacancy_phone)
                    phone.phone = ",".join(phones)
                    try:
                        update_bitrix_contact(phone.bitrix_id, phone.phone)
                        session.commit()
                    except:
                        pass

                vacancy = Vacancy(
                    name=vacancy_data["name"],
                    phone=phone,
                    company=company,
                    url=vacancy_data["url"],
                    date=today,
                )
                try:
                    add_bitrix_lead(
                        vacancy_data["name"],
                        phone.bitrix_id,
                        company.bitrix_id,
                        vacancy_data["url"],
                    )
                except Exception as e:
                    print("ОШИБКА С ДОБАВЛЕНИЕМ ЛИДА В БИТРИКС", e)

                    continue
                session.add(vacancy)
                company.vacancies.append(vacancy)
                vacancies_added += 1
                session.commit()

    print(f"Companies added: {companies_added}")
    print(f"Vacancies added: {vacancies_added}")
