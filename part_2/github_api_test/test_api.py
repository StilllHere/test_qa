import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_USER = os.getenv('GITHUB_USER')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')


def create_repo():
    url = "https://api.github.com/user/repos"
    response = requests.post(url, json={"name": REPO_NAME, "private": False}, auth=(GITHUB_USER, GITHUB_TOKEN))
    return response


def repo_exists():
    url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}"
    response = requests.get(url, auth=(GITHUB_USER, GITHUB_TOKEN))
    return response.status_code == 200


def delete_repo():
    url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}"
    response = requests.delete(url, auth=(GITHUB_USER, GITHUB_TOKEN))
    return response.status_code


def test_github_repo():
    print("Проверка наличия репозитория...")
    if repo_exists():
        print("Репозиторий уже существует. Удаляем его...")
        status_code = delete_repo()
        if status_code != 204:
            print("Не удалось удалить репозиторий. Проверьте права доступа или существование репозитория.")
            return  # Завершаем выполнение, если репозиторий не удален

    print("Создание репозитория...")
    create_response = create_repo()

    if create_response.status_code == 201:
        print(f"Созданный репозиторий: {create_response.json().get('name')}")
    else:
        print(f"Ошибка создания репозитория: {create_response.json()}")
        return

    print("Проверка наличия репозитория...")
    assert repo_exists(), "Репозиторий не был найден."

    print("Удаление репозитория...")
    status_code = delete_repo()
    assert status_code == 204, "Не удалось удалить репозиторий."
    print("Репозиторий успешно удален.")


if __name__ == "__main__":
    test_github_repo()
