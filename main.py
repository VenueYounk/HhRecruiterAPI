from flask import Flask, jsonify, request, render_template
from pytz import timezone
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler


from modules.utils.update_database import update_database
from modules.database.models import session, Company, Phones

from modules.database.func_db import add_data

import requests

import sys


# if "-test" in sys.argv:
#     count = 1
#     while True:
#         test = requests.get(
#             f"http://85.198.90.82:8000/companies?sort_by=name&page={count}&results_per_page=300"
#         ).json()
#         if test != []:
#             count += 1
#         else:
#             break
#         print(count)
#         # print(test)
#         add_data(test)


if "-scan" in sys.argv:
    update_database()
    # print("This fucntion are started")


app = Flask(__name__)
scheduler = BackgroundScheduler(timezone=timezone("Asia/Almaty"))
scheduler.start()


@app.route("/")
def main_page():
    return render_template("index.html")


# Route to get all todos
@app.route("/companies", methods=["GET"])
def get_companies():
    page = int(request.args.get("page", 1))
    results_per_page = int(request.args.get("results_per_page", 50))
    sort_by = request.args.get("sort_by", "industries")
    search_text = request.args.get("search_text", "")

    companies_query = session.query(Company).order_by(getattr(Company, sort_by))

    if search_text:
        companies_query = companies_query.filter(
            Company.name.ilike(f"%{search_text}%")
            | Company.industries.ilike(f"%{search_text}%")
        )

    companies = (
        companies_query.offset((page - 1) * results_per_page)
        .limit(results_per_page)
        .all()
    )

    companies_query = companies_query.filter(Company.vacancies.any())

    company_list = []

    for company in companies:
        if company == []:
            continue
        vacancies = [
            {
                "name": vacancy.name,
                "contact_name": vacancy.contact_name,
                "phone": vacancy.phone,
                "url": vacancy.url,
            }
            for vacancy in company.vacancies
        ]

        company_info = {
            "company_name": company.name,
            "industry": company.industries,
            "vacancies": vacancies,
        }

        company_list.append(company_info)

    return jsonify(company_list)


@app.route("/phones")
def get_phones():
    page = int(request.args.get("page", 1))
    results_per_page = int(request.args.get("results_per_page", 50))
    sort_by = request.args.get("sort_by", "name")
    search_text = request.args.get("search_text", "")

    companies_query = session.query(Company).order_by(getattr(Company, sort_by))

    if search_text:
        companies_query = companies_query.filter(
            Company.name.ilike(f"%{search_text}%")
            | Company.industries.ilike(f"%{search_text}%")
        )

    companies = (
        companies_query.offset((page - 1) * results_per_page)
        .limit(results_per_page)
        .all()
    )

    company_list = []

    for company in companies:
        phones = [
            {
                "name": phone.name,
                "phone": phone.phone,
            }
            for phone in company.phones
        ]

        company_info = {
            "company_name": company.name,
            "industry": company.industries,
            "phones": phones,
        }

        company_list.append(company_info)

    return jsonify(company_list)


scheduler.add_job(update_database, "cron", day_of_week="*", hour=1, minute=0, second=0)


if __name__ == "__main__":
    app.run(debug=False)
