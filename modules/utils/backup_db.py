import os
import shutil
from datetime import datetime, timedelta


def delete_old_backups(backup_dir, days=3):
    # Получаем текущую дату
    now = datetime.now()

    # Проходим по всем файлам в директории бэкапа
    for filename in os.listdir(backup_dir):
        # Получаем полный путь к файлу
        file_path = os.path.join(backup_dir, filename)

        # Получаем время последней модификации файла
        file_time = datetime.fromtimestamp(os.path.getmtime(file_path))

        # Если файл старше указанного количества дней, удаляем его
        if now - file_time > timedelta(days=days):
            os.remove(file_path)
            print(f"Deleted old backup: {file_path}")


def backup_db():
    # Path to the original SQLite database file
    original_db_path = "./database.db"

    # Create a backup directory if it doesn't exist
    backup_dir = "./backup"
    os.makedirs(backup_dir, exist_ok=True)

    # Generate the backup file name with current date
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file_name = f"database_backup_{current_date}.db"
    backup_db_path = os.path.join(backup_dir, backup_file_name)

    # Copy the original database file to the backup file
    shutil.copyfile(original_db_path, backup_db_path)
    print(f"Backup created: {backup_db_path}")

    # Удаляем старые бэкапы
    delete_old_backups(backup_dir)
