import random
from datetime import datetime

from support_platform.models.operator import Operator
from support_platform.models.user import User
from support_platform.models.chat import Chat


class SupportPlatform:
    """Платформа для обработки обращений в поддержку."""

    def __init__(self):
        self.operators: list[Operator] = []
        self.users: list[User] = []
        self.chats: list[Chat] = []
        self._next_chat_id = 1  # счётчик для автоинкремента id чатов

    # --- Регистрация ---

    def register_operator(self, operator: Operator):
        """Добавить оператора на платформу."""
        self.operators.append(operator)

    def register_user(self, user: User):
        """Добавить пользователя на платформу."""
        self.users.append(user)

    # --- Создание обращения ---

    def create_chat(self, user: User, created_at: datetime = None) -> Chat:
        """Создать чат - выбирает случайного свободного оператора."""
        available = self.get_available_operators()
        if not available:
            raise RuntimeError("Нет свободных операторов для обработки обращения")

        operator = random.choice(available)
        operator.set_busy()

        chat = Chat(self._next_chat_id, user, operator, created_at)
        self.chats.append(chat)
        self._next_chat_id += 1

        return chat

    # --- Получение данных ---

    def get_available_operators(self) -> list[Operator]:
        """Список свободных операторов, готовых принять чат."""
        return [op for op in self.operators if op.is_available]

    def get_chats_by_operator(self, operator_id: int) -> list[Chat]:
        """Все чаты конкретного оператора (по id)."""
        return [c for c in self.chats if c.operator.person_id == operator_id]

    def get_chats_by_user(self, user_id: int) -> list[Chat]:
        """Все чаты конкретного пользователя (по id)."""
        return [c for c in self.chats if c.user.person_id == user_id]

    def get_all_chats(self) -> list[Chat]:
        """Все чаты платформы."""
        return self.chats

    def get_operator_profiles(self) -> list[dict]:
        """Профили всех операторов (список словарей для выгрузки)."""
        return [op.to_dict() for op in self.operators]

    def get_user_profiles(self) -> list[dict]:
        """Профили всех пользователей (список словарей для выгрузки)."""
        return [u.to_dict() for u in self.users]

    def __str__(self) -> str:
        open_count = sum(1 for c in self.chats if c.status == "open")
        closed_count = sum(1 for c in self.chats if c.status == "closed")
        return (
            f"Платформа: {len(self.operators)} операторов, "
            f"{len(self.users)} пользователей, "
            f"{len(self.chats)} чатов "
            f"(открытых: {open_count}, закрытых: {closed_count})"
        )
