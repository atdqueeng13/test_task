from datetime import datetime

from support_platform.models.message import Message
from support_platform.models.user import User
from support_platform.models.operator import Operator


class Chat:
    """Чат (обращение) в поддержку."""

    # время можно не передавать - тогда берётся текущее.
    # Генератор передаёт своё, см. simulate_chats()

    def __init__(self, chat_id: int, user: User, operator: Operator,
                 created_at: datetime = None):
        self.chat_id = chat_id
        self.user = user
        self.operator = operator
        self.messages: list[Message] = []
        self.status = "open"
        self.csat = None  # оценка от 1 до 5, проставляется после закрытия
        self.created_at = created_at or datetime.now()
        self.closed_at = None

    def add_message(self, text: str, sender_name: str, sender_role: str,
                    timestamp: datetime = None):
        """Добавить сообщение в чат. В закрытый чат писать нельзя."""
        if self.status == "closed":
            raise ValueError(
                f"Чат #{self.chat_id} закрыт, отправка сообщений невозможна"
            )

        message = Message(text, sender_name, sender_role, timestamp)
        self.messages.append(message)
        return message

    def send_user_message(self, text: str, timestamp: datetime = None):
        """Отправить сообщение от имени пользователя."""
        return self.add_message(text, self.user.username, "user", timestamp)

    def send_operator_message(self, text: str, timestamp: datetime = None):
        """Отправить сообщение от имени оператора."""
        return self.add_message(
            text, self.operator.full_name, "operator", timestamp
        )

    def close(self, closed_at: datetime = None):
        """Закрыть чат. После закрытия оператор освобождается."""
        if self.status == "closed":
            raise ValueError(f"Чат #{self.chat_id} уже закрыт")

        self.status = "closed"
        self.closed_at = closed_at or datetime.now()
        self.operator.set_available()

    def set_csat(self, score: int):
        """Проставить оценку CSAT (от 1 до 5). Только после закрытия чата."""
        if self.status != "closed":
            raise ValueError(
                f"Чат #{self.chat_id} ещё открыт, оценка невозможна"
            )
        if not (1 <= score <= 5):
            raise ValueError(
                f"CSAT должен быть от 1 до 5, получено: {score}"
            )
        if self.csat is not None:
            raise ValueError(
                f"Чат #{self.chat_id} уже оценён (csat={self.csat})"
            )
        self.csat = score

    def to_dict(self) -> dict:
        """Полные данные чата в виде словаря (для JSON-выгрузки)."""
        return {
            "chat_id": self.chat_id,
            "status": self.status,
            "user": self.user.to_dict(),
            "operator": self.operator.to_dict(),
            "messages": [m.to_dict() for m in self.messages],
            "csat": self.csat,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "closed_at": (
                self.closed_at.strftime("%Y-%m-%d %H:%M:%S")
                if self.closed_at else None
            ),
        }

    def __str__(self) -> str:
        msgs_count = len(self.messages)
        csat_str = self.csat if self.csat else "нет"
        return (
            f"Чат #{self.chat_id} [{self.status}] - "
            f"{self.user.username} <-> {self.operator.full_name} "
            f"(сообщений: {msgs_count}, csat: {csat_str})"
        )

    def __repr__(self) -> str:
        return (
            f"Chat(id={self.chat_id}, status='{self.status}', "
            f"user='{self.user.username}', "
            f"operator='{self.operator.full_name}')"
        )
