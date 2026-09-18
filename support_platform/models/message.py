from datetime import datetime


class Message:
    """Сообщение в чате поддержки."""

    def __init__(self, text: str, sender_name: str, sender_role: str,
                 timestamp: datetime = None):
        # sender_role = 'user' или 'operator'
        self.text = text
        self.sender_name = sender_name
        self.sender_role = sender_role
        self.timestamp = timestamp or datetime.now()

    def to_dict(self) -> dict:
        """Словарь для JSON-выгрузки."""
        return {
            "text": self.text,
            "sender_name": self.sender_name,
            "sender_role": self.sender_role,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def __str__(self) -> str:
        time_str = self.timestamp.strftime("%H:%M")
        return f"[{time_str}] {self.sender_name}: {self.text}"

    def __repr__(self) -> str:
        return (
            f"Message(sender='{self.sender_name}', "
            f"role='{self.sender_role}', text='{self.text[:30]}...')"
        )
