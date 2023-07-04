from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from modules.database.models import Company, Vacancy, Phones, session

# import logging

# logging.disable(logging.WARNING)

# Create a SQLite database engine and session


def drop_tables():
    # session.query(Company).delete()
    session.query(Vacancy).delete()
    session.commit()


# Function to add data to the database
def add_data(data):
    companies_added = 0
    vacancies_added = 0

    for comp in data:
        company = session.query(Company).filter_by(name=comp["name"]).first()

        if company is None:
            company = Company(name=comp["name"], industries=comp["industries"])
            session.add(company)
            companies_added += 1

        for vacancy_data in comp["vacancies"]:
            vacancy = (
                session.query(Vacancy)
                .filter_by(name=vacancy_data["name"], company_id=company.id)
                .first()
            )

            if vacancy is None:
                vacancy = Vacancy(
                    name=vacancy_data["name"],
                    contact_name=vacancy_data["contact_name"],
                    phone=vacancy_data["phone"],
                    company_id=company.id,
                    url=vacancy_data["url"],
                )
                company.vacancies.append(vacancy)
                session.add(vacancy)
                vacancies_added += 1

    session.commit()

    print(f"Companies added: {companies_added}")
    print(f"Vacancies added: {vacancies_added}")


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
