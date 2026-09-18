# Сценарий 1: создание 120 чатов, примеры переписки, обновление данных.
# Запуск: python scripts/demo_create_chats.py

import sys
import os

# чтобы импорты работали из корня проекта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.stdout.reconfigure(encoding="utf-8")

from support_platform import SupportPlatform
from support_platform.generator import populate_platform, simulate_chats
from run import print_statistics  # scripts/run.py лежит рядом


def print_chat(title, chat):
    """Вывести чат со всей перепиской."""
    print(f"\n--- {title} ---")
    print(chat)
    for message in chat.messages:
        print(f"  {message}")


def main():
    platform = SupportPlatform()
    populate_platform(platform, n_operators=15, n_users=50)
    created = simulate_chats(platform, n_chats=120)
    print(f"Создано {created} чатов")

    print_statistics(platform)

    # по одному примеру чата каждого вида
    rated = None
    not_rated = None
    opened = None
    for chat in platform.chats:
        if chat.status == "open":
            if opened is None:
                opened = chat
        elif chat.csat is None:
            if not_rated is None:
                not_rated = chat
        elif rated is None:
            rated = chat

    print("Примеры чатов:")
    if rated:
        print_chat("закрыт с CSAT", rated)
    if not_rated:
        print_chat("закрыт без CSAT", not_rated)
    if opened:
        print_chat("открыт", opened)

    # обновление данных: пользователь переехал, оператора повысили
    print("\nАктуализация данных:")
    user = platform.users[0]
    print(f"  до:    {user.full_name}, {user.city}")
    user.update(city="Казань")
    print(f"  после: {user.full_name}, {user.city}")

    operator = platform.operators[0]
    print(f"  до:    {operator}, стаж {operator.experience_years}")
    operator.update(position="Старший оператор",
                    experience_years=operator.experience_years + 1)
    print(f"  после: {operator}, стаж {operator.experience_years}")


if __name__ == "__main__":
    main()
