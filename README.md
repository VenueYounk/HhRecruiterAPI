# HeadHunter Recruiter API

This is API + parser.

client_id and secret_id from dev.hh.ru are required.

## Parser

Every night this script, deep enough and scans the available vacancies with contact details, and saves them to the database

Every night, the database is deleted and filled with up-to-date data.

However, phone numbers are stored in a separate table so that no number is ever lost.

## API Usage Documentation

### Get Companies

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>request</span><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">GET /companies
</code></div></div></pre>

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

### Get Phones

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>request</span><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">GET /phones
</code></div></div></pre>

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
