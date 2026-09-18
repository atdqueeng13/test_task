import json
import os


def _save_and_print(data: list[dict], filename: str, title: str):
    """
    Общая логика выгрузки: сохранить в JSON-файл + вывести в консоль.
    Создаёт папку exports/ если её нет.
    """
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"  Записей: {len(data)}")
    print(f"  Сохранено в: {filename}")
    print(f"{'=' * 60}")

    # в консоль - только первые 3 записи, остальное в файле
    preview_count = min(3, len(data))
    for i, item in enumerate(data[:preview_count]):
        print(f"\n--- Запись {i + 1} ---")
        _print_dict(item)

    if len(data) > preview_count:
        print(f"\n... и ещё {len(data) - preview_count} записей (см. файл)")
    print()


def _print_dict(d: dict, indent: int = 0):
    """Красивый вывод словаря в консоль (без вложенных списков целиком)."""
    prefix = "  " * indent
    for key, value in d.items():
        if isinstance(value, dict):
            print(f"{prefix}{key}:")
            _print_dict(value, indent + 1)
        elif isinstance(value, list):
            print(f"{prefix}{key}: [{len(value)} шт.]")
        else:
            print(f"{prefix}{key}: {value}")


# --- Выгрузка чатов ---

def export_all_chats(platform, filename: str = "exports/all_chats.json"):
    """Выгрузить все чаты платформы."""
    data = [chat.to_dict() for chat in platform.get_all_chats()]
    _save_and_print(data, filename, "Все чаты платформы")
    return data


def export_chats_by_operator(platform, operator_id: int,
                              filename: str = None):
    """Выгрузить чаты конкретного оператора."""
    if filename is None:
        filename = f"exports/operator_{operator_id}_chats.json"

    chats = platform.get_chats_by_operator(operator_id)
    data = [chat.to_dict() for chat in chats]

    # находим имя оператора для заголовка
    op_name = f"оператор #{operator_id}"
    for op in platform.operators:
        if op.person_id == operator_id:
            op_name = op.full_name
            break

    _save_and_print(data, filename, f"Чаты оператора: {op_name}")
    return data


def export_chats_by_user(platform, user_id: int,
                          filename: str = None):
    """Выгрузить чаты конкретного пользователя."""
    if filename is None:
        filename = f"exports/user_{user_id}_chats.json"

    chats = platform.get_chats_by_user(user_id)
    data = [chat.to_dict() for chat in chats]

    # находим имя пользователя для заголовка
    u_name = f"пользователь #{user_id}"
    for u in platform.users:
        if u.person_id == user_id:
            u_name = f"{u.username} ({u.full_name})"
            break

    _save_and_print(data, filename, f"Чаты пользователя: {u_name}")
    return data


# --- Выгрузка профилей ---

def export_operator_profiles(platform,
                              filename: str = "exports/operators.json"):
    """Выгрузить профили всех операторов."""
    data = platform.get_operator_profiles()
    _save_and_print(data, filename, "Профили операторов")
    return data


def export_user_profiles(platform,
                          filename: str = "exports/users.json"):
    """Выгрузить профили всех пользователей."""
    data = platform.get_user_profiles()
    _save_and_print(data, filename, "Профили пользователей")
    return data
