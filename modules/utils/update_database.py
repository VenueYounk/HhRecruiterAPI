from modules.database.func_db import add_data, save_phones, drop_tables
from modules.utils.backup_db import backup_db
from modules.parser.hh_api import HHAPI


def update_database():
    print("This fucntion are started")
    backup_db()
    parser = HHAPI()
    drop_tables()
    dataset = parser.get_vacancies_from_employers()
    add_data(dataset)
    dataset = parser.get_employers_by_vacancy()
    add_data(dataset)
    save_phones()
