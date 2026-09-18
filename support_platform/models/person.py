from datetime import date


class Person:
    """Базовый класс человека на платформе (оператор или пользователь)."""

    def __init__(
        self,
        person_id: int,
        last_name: str,
        first_name: str,
        patronymic: str,
        city: str,
        birth_date: date,
        position: str,
        experience_years: int,  # стаж в годах
    ):
        self.person_id = person_id
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.city = city
        self.birth_date = birth_date
        self.position = position
        self.experience_years = experience_years

    @property
    def full_name(self) -> str:
        """ФИО в формате 'Фамилия Имя Отчество'."""
        return f"{self.last_name} {self.first_name} {self.patronymic}"

    @property
    def age(self) -> int:
        """Возраст в полных годах (считаем от даты рождения)."""
        today = date.today()
        age = today.year - self.birth_date.year
        # если день рождения в этом году ещё не наступил - вычитаем год
        if today.month < self.birth_date.month:
            age -= 1
        elif today.month == self.birth_date.month and today.day < self.birth_date.day:
            age -= 1
        return age

    # поля, которые можно менять через update()
    # id не трогаем, а занятость оператора меняется сама при открытии/закрытии чата
    UPDATABLE_FIELDS = [
        "last_name", "first_name", "patronymic", "city",
        "birth_date", "position", "experience_years",
    ]

    def update(self, **fields):
        """
        Обновить данные человека, например:
        person.update(city="Казань", experience_years=5)
        """
        # проверяем все поля до изменений, чтобы не обновить данные наполовину
        for key in fields:
            if key not in self.UPDATABLE_FIELDS:
                raise ValueError(f"Поле {key} нельзя изменить")
        if "experience_years" in fields and fields["experience_years"] < 0:
            raise ValueError("Стаж не может быть отрицательным")

        for key, value in fields.items():
            setattr(self, key, value)

    def to_dict(self) -> dict:
        """Конвертация в словарь (для выгрузки в JSON)."""
        return {
            "id": self.person_id,
            "full_name": self.full_name,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "patronymic": self.patronymic,
            "city": self.city,
            "birth_date": self.birth_date.isoformat(),
            "age": self.age,
            "position": self.position,
            "experience_years": self.experience_years,
        }

    def __str__(self) -> str:
        return f"{self.full_name} ({self.position})"

    def __repr__(self) -> str:
        return (
            f"Person(id={self.person_id}, name='{self.full_name}', "
            f"city='{self.city}', position='{self.position}')"
        )
