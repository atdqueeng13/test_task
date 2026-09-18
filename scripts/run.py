# Полный цикл: генерация, симуляция чатов, статистика, все выгрузки.
# Запуск: python scripts/run.py

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


def print_statistics(platform):
    """Вывод общей статистики по платформе."""
    all_chats = platform.get_all_chats()
    closed_chats = [c for c in all_chats if c.status == "closed"]
    open_chats = [c for c in all_chats if c.status == "open"]
    rated_chats = [c for c in closed_chats if c.csat is not None]

    print("\n" + "=" * 60)
    print("  СТАТИСТИКА ПЛАТФОРМЫ")
    print("=" * 60)
    print(f"  Операторов:    {len(platform.operators)}")
    print(f"  Пользователей: {len(platform.users)}")
    print(f"  Всего чатов:   {len(all_chats)}")
    print(f"    - открытых:  {len(open_chats)}")
    print(f"    - закрытых:  {len(closed_chats)}")
    print(f"    - с оценкой: {len(rated_chats)}")

    if rated_chats:
        avg_csat = sum(c.csat for c in rated_chats) / len(rated_chats)
        print(f"  Средний CSAT:  {avg_csat:.2f}")

    total_msgs = sum(len(c.messages) for c in all_chats)
    print(f"  Всего сообщений: {total_msgs}")

    print("\n  Топ-3 оператора по чатам:")
    op_stats = []
    for op in platform.operators:
        op_chats = platform.get_chats_by_operator(op.person_id)
        op_stats.append((op, len(op_chats)))
    op_stats.sort(key=lambda x: x[1], reverse=True)

    for i, (op, count) in enumerate(op_stats[:3], 1):
        print(f"    {i}. {op.full_name} - {count} чатов")

    print()


def main():
    print("Запуск платформы поддержки...\n")

    platform = SupportPlatform()

    print("Генерация операторов и пользователей...")
    populate_platform(platform, n_operators=15, n_users=50)
    print(f"  Создано {len(platform.operators)} операторов")
    print(f"  Создано {len(platform.users)} пользователей")

    print("\nСимуляция чатов...")
    created = simulate_chats(platform, n_chats=120)
    print(f"  Создано {created} чатов")

    print_statistics(platform)

    print("Запуск выгрузок...")
    export_all_chats(platform)
    export_operator_profiles(platform)
    export_user_profiles(platform)

    # для примера - чаты первого оператора и первого пользователя
    export_chats_by_operator(platform, platform.operators[0].person_id)
    export_chats_by_user(platform, platform.users[0].person_id)

    print("\nГотово! Все данные сохранены в папке exports/")


if __name__ == "__main__":
    main()
