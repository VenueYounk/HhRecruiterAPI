import os
import shutil
from datetime import datetime


def backup_db():
    # Path to the original SQLite database file
    original_db_path = "./database.db"

    # Create a backup directory if it doesn't exist
    backup_dir = "./backup"
    os.makedirs(backup_dir, exist_ok=True)

    # Generate the backup file name with current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    backup_file_name = f"database_backup_{current_date}.db"
    backup_db_path = os.path.join(backup_dir, backup_file_name)

    # Copy the original database file to the backup file
    shutil.copyfile(original_db_path, backup_db_path)
    print(f"Backup created: {backup_db_path}")
