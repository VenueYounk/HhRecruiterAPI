# HeadHunter Recruiter API

### What is it?

This is API + parser.

client_id and secret_id from dev.hh.ru are required.

## Install&Run

### Install

```bash
git clone https://github.com/VenueYounk/HhRecruiterAPI

pip install -r requirements.txt
```

### Run

#### Standart run

```bash
python3 main.py
```

#### Run with parsing data

```bash
python3 main.py -scan
```

## Parser

Every night this script, deep enough and scans the available vacancies with contact details, and saves them to the database

Every night, the database is deleted and filled with up-to-date data.

However, phone numbers are stored in a separate table so that no number is ever lost.

## API Usage Documentation

### Get Companies

`GET /companies`

Retrieves a list of companies with options for filtering and pagination.

#### Request Parameters

* `page` (optional): The page number of the results (default: 1).
* `results_per_page` (optional): The number of results per page (default: 50).
* `sort_by` (optional): The field to sort the results by (default: industries).
* `search_text` (optional): Text to search for in the company name or industries.

#### Response

The API response will be a JSON object containing a list of companies. Each company object will have the following properties:

* `company_name`: The name of the company.
* `industry`: The industry of the company.
* `vacancies`: A list of vacancies within the company. Each vacancy object will have the following properties:
  * `name`: The name of the vacancy.
  * `contact_name`: The name of the contact person for the vacancy.
  * `phone`: The phone number for the vacancy.

#### Response Example

```json
[
  {
    "company_name":"Example Company 1",
    "industry":"Technology",
    "vacancies":[
      {
        "name":"Software Engineer",
        "contact_name":"John Doe",
        "phone":"+1234567890"
      },
      {
        "name":"Project Manager",
        "contact_name":"Jane Smith",
        "phone":"+9876543210"
      }
    ]
  },
  {
    "company_name":"Example Company 2",
    "industry":"Finance",
    "vacancies":[
      {
        "name":"Financial Analyst",
        "contact_name":"Mark Johnson",
        "phone":"+2468135790"
      }
    ]
  }
]
```

### Get Phones

`GET /phones`

Retrieves a list of companies with their associated phone numbers.

#### Request Parameters

* `page` (optional): The page number of the results (default: 1).
* `results_per_page` (optional): The number of results per page (default: 50).
* `sort_by` (optional): The field to sort the results by (default: name).
* `search_text` (optional): Text to search for in the company name or industries.

#### Response

The API response will be a JSON object containing a list of companies. Each company object will have the following properties:

* `company_name`: The name of the company.
* `industry`: The industry of the company.
* `phones`: A list of phone numbers associated with the company. Each phone number object will have the following properties:
  * `name`: The name of the phone number (e.g., "Sales Department", "Technical Support").
  * `phone`: The phone number.

#### Response Example

```json
[
  {
    "company_name": "Example Company 1",
    "industry": "Technology",
    "phones": [
      {
        "name": "Vasya Pupkin",
        "phone": "+1234567890"
      },
      {
        "name": "Dondon Herovich",
        "phone": "+9876543210"
      }
    ]
  },
  {
    "company_name": "Example Company 2",
    "industry": "Finance",
    "phones": [
      {
        "name": "WhyAreYou Runningovich",
        "phone": "+2468135790"
      }
    ]
  }
]

```
