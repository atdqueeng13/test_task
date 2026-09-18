# Сценарий 2: все 5 видов выгрузок.
# Запуск: python scripts/demo_export.py

import sys
import os

# чтобы импорты работали из корня проекта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.stdout.reconfigure(encoding="utf-8")

from support_platform import SupportPlatform
from support_platform.generator import populate_platform, simulate_chats
from support_platform.exporter import (
    export_all_chats, export_chats_by_operator,
    export_chats_by_user, export_operator_profiles, export_user_profiles,
)


def main():
    platform = SupportPlatform()
    populate_platform(platform, n_operators=15, n_users=50)
    simulate_chats(platform, n_chats=120)

    export_all_chats(platform)

    # для примера - чаты первого оператора и первого пользователя
    export_chats_by_operator(platform, platform.operators[0].person_id)
    export_chats_by_user(platform, platform.users[0].person_id)

    export_operator_profiles(platform)
    export_user_profiles(platform)

    print("Готово! Все выгрузки сохранены в папке exports/")


if __name__ == "__main__":
    main()
