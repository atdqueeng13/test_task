from datetime import date

from support_platform.models.person import Person


class User(Person):
    """Пользователь платформы. Создаёт обращения и ставит оценку (CSAT)."""

    # пользователю дополнительно можно сменить ник
    UPDATABLE_FIELDS = Person.UPDATABLE_FIELDS + ["username"]

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
        username: str,
    ):
        super().__init__(
            person_id, last_name, first_name, patronymic,
            city, birth_date, position, experience_years,
        )
        self.username = username

    def to_dict(self) -> dict:
        """Словарь с данными пользователя для JSON-выгрузки."""
        data = super().to_dict()
        data["username"] = self.username
        return data

    def __str__(self) -> str:
        return f"{self.username} - {self.full_name} ({self.position})"

    def __repr__(self) -> str:
        return (
            f"User(id={self.person_id}, username='{self.username}', "
            f"name='{self.full_name}')"
        )
