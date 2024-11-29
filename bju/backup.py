import os
import subprocess
import requests
from datetime import datetime

from bju.config import OAUTH_TOKEN, DB_USER, DB_NAME, YANDEX_DISK_URL

# Конфигурация
DB_NAME = DB_NAME
DB_USER = DB_USER
YANDEX_DISK_URL = YANDEX_DISK_URL
OAUTH_TOKEN = OAUTH_TOKEN

def create_dump():
    """Создать дамп базы данных."""
    # Формирование уникального имени файла
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = f"backup_{timestamp}.sql"

    try:
        subprocess.run(
            [
                "/opt/homebrew/bin/pg_dump",
                "-U", DB_USER,
                "-F", "c",  # Формат custom
                "-b",  # Инклюзия больших объектов
                "-v",  # Подробный вывод
                "-f", backup_file,
                DB_NAME,
            ],
            check=True,
        )
        print(f"Дамп {backup_file} успешно создан!")
        return backup_file
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании дампа: {e}")
        raise

def upload_to_yandex_disk(local_path, remote_path):
    """Загрузить файл на Яндекс.Диск."""
    headers = {"Authorization": f"OAuth {OAUTH_TOKEN}"}

    # Запрос URL для загрузки
    params = {"path": remote_path, "overwrite": "true"}
    response = requests.get(YANDEX_DISK_URL, headers=headers, params=params)
    response.raise_for_status()
    upload_url = response.json().get("href")

    # Загрузка файла
    with open(local_path, "rb") as f:
        response = requests.put(upload_url, files={"file": f})
        response.raise_for_status()
        print(f"Файл {local_path} успешно загружен на Яндекс.Диск по пути {remote_path}!")

if __name__ == "__main__":
    try:
        # Создание дампа
        backup_file = create_dump()

        # Загрузка дампа на Яндекс.Диск
        remote_path = f"/backups/{backup_file}"
        upload_to_yandex_disk(backup_file, remote_path)
    finally:
        # Удаление локального файла после загрузки
        if os.path.exists(backup_file):
            os.remove(backup_file)
            print(f"Локальный файл {backup_file} успешно удален.")