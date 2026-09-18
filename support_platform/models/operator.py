from datetime import date

from support_platform.models.person import Person


class Operator(Person):
    """Оператор поддержки. Обрабатывает обращения пользователей."""

    def __init__(
        self,
        person_id: int,
        last_name: str,
        first_name: str,
        patronymic: str,
        city: str,
        birth_date: date,
        position: str,
        experience_years: int,
    ):
        super().__init__(
            person_id, last_name, first_name, patronymic,
            city, birth_date, position, experience_years,
        )
        self.is_available = True

    def set_busy(self):
        """Пометить оператора как занятого (назначен на чат)."""
        self.is_available = False

    def set_available(self):
        """Освободить оператора (чат закрыт, можно брать новый)."""
        self.is_available = True

    def to_dict(self) -> dict:
        """Словарь с данными оператора для JSON-выгрузки."""
        data = super().to_dict()
        data["is_available"] = self.is_available
        return data

    def __str__(self) -> str:
        status = "свободен" if self.is_available else "занят"
        return f"{self.full_name} ({self.position}) - {status}"

    def __repr__(self) -> str:
        return (
            f"Operator(id={self.person_id}, name='{self.full_name}', "
            f"available={self.is_available})"
        )
