import random
from datetime import date, datetime, timedelta

from support_platform.models.operator import Operator
from support_platform.models.user import User


# --- Заготовленные списки ---

MALE_FIRST_NAMES = [
    "Александр", "Дмитрий", "Максим", "Иван", "Артём",
    "Сергей", "Андрей", "Алексей", "Никита", "Михаил",
    "Даниил", "Егор", "Роман", "Владимир", "Павел",
    "Кирилл", "Тимофей", "Матвей", "Илья", "Олег",
]

FEMALE_FIRST_NAMES = [
    "Анна", "Мария", "Елена", "Ольга", "Наталья",
    "Екатерина", "Татьяна", "Ирина", "Светлана", "Юлия",
    "Дарья", "Алина", "Виктория", "Полина", "Ксения",
    "Валерия", "Софья", "Вероника", "Кристина", "Марина",
]

MALE_PATRONYMICS = [
    "Александрович", "Дмитриевич", "Сергеевич", "Иванович",
    "Андреевич", "Алексеевич", "Николаевич", "Михайлович",
    "Владимирович", "Олегович", "Павлович", "Игоревич",
    "Петрович", "Романович", "Юрьевич",
]

FEMALE_PATRONYMICS = [
    "Александровна", "Дмитриевна", "Сергеевна", "Ивановна",
    "Андреевна", "Алексеевна", "Николаевна", "Михайловна",
    "Владимировна", "Олеговна", "Павловна", "Игоревна",
    "Петровна", "Романовна", "Юрьевна",
]

LAST_NAMES_MALE = [
    "Иванов", "Петров", "Сидоров", "Козлов", "Смирнов",
    "Кузнецов", "Попов", "Васильев", "Соколов", "Михайлов",
    "Новиков", "Фёдоров", "Морозов", "Волков", "Алексеев",
    "Лебедев", "Семёнов", "Егоров", "Павлов", "Степанов",
    "Николаев", "Орлов", "Макаров", "Захаров", "Зайцев",
]

LAST_NAMES_FEMALE = [
    "Иванова", "Петрова", "Сидорова", "Козлова", "Смирнова",
    "Кузнецова", "Попова", "Васильева", "Соколова", "Михайлова",
    "Новикова", "Фёдорова", "Морозова", "Волкова", "Алексеева",
    "Лебедева", "Семёнова", "Егорова", "Павлова", "Степанова",
    "Николаева", "Орлова", "Макарова", "Захарова", "Зайцева",
]

CITIES = [
    "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург",
    "Казань", "Нижний Новгород", "Челябинск", "Самара",
    "Омск", "Ростов-на-Дону", "Уфа", "Красноярск",
    "Воронеж", "Пермь", "Волгоград", "Краснодар",
    "Тюмень", "Саратов", "Тольятти", "Ижевск",
]

# должности для операторов
OPERATOR_POSITIONS = [
    "Оператор поддержки", "Старший оператор", "Специалист поддержки",
    "Менеджер поддержки", "Оператор контакт-центра",
]

# должности для пользователей - кем они работают в жизни
USER_POSITIONS = [
    "Менеджер", "Аналитик", "Разработчик", "Дизайнер",
    "Бухгалтер", "Инженер", "Преподаватель", "Врач",
    "Юрист", "Маркетолог", "Студент", "Продавец",
    "Логист", "Администратор", "Экономист",
]

# --- Шаблоны сообщений ---

# первое сообщение пользователя (с чего начинается обращение)
USER_OPENING_MESSAGES = [
    "Здравствуйте, не доставили заказ",
    "Добрый день, курьер не приехал",
    "Привет, заказ приехал холодным",
    "Заказ приехал, но не хватает одной позиции",
    "Курьер привёз не тот заказ",
    "Здравствуйте, хочу отменить заказ",
    "Не могу оформить заказ, приложение выдаёт ошибку",
    "Добрый день, списали деньги, а заказ не оформился",
    "Привезли заказ с опозданием на час",
    "Здравствуйте, еда была испорчена",
    "Не могу применить промокод",
    "Курьер нагрубил, хочу пожаловаться",
    "Заказ показывает статус 'доставлен', но мне ничего не привезли",
    "Добрый день, можно ли изменить адрес доставки?",
    "Не приходит СМС с кодом подтверждения",
    "Подскажите, как вернуть деньги за заказ?",
    "Заказ потерялся, трекер не обновляется уже 40 минут",
    "Привезли остывшую пиццу, просил горячую",
]

# ответы оператора
OPERATOR_MESSAGES = [
    "Добрый день! Подскажите, пожалуйста, номер заказа",
    "Здравствуйте! Уточните, пожалуйста, номер вашего заказа",
    "Приносим извинения за неудобства! Сейчас разберёмся",
    "Спасибо за обращение. Проверяю информацию по вашему заказу",
    "Очень жаль, что так вышло. Уже передал вопрос в нужный отдел",
    "Оформил возврат, деньги поступят в течение 3 рабочих дней",
    "Начислил вам промокод на следующий заказ в качестве компенсации",
    "Проблема решена! Могу ещё чем-то помочь?",
    "К сожалению, отменить заказ на этом этапе уже нельзя",
    "Передал информацию курьерской службе, с вами свяжутся",
    "Спасибо за ожидание! Разобрался в ситуации",
    "Повторная доставка будет в течение 40 минут",
]

# продолжение диалога от пользователя
USER_FOLLOWUP_MESSAGES = [
    "Спасибо!",
    "Хорошо, жду",
    "Понял, спасибо за помощь",
    "А сколько ждать возврат?",
    "Ладно, тогда ок",
    "Номер заказа #{}",  # номер подставляется в random_user_followup()
    "Да, всё верно",
    "Нет, проблема не решена",
    "Ок, буду ждать",
    "Спасибо, вопросов больше нет",
    "А промокод на какую сумму?",
    "Это уже не первый раз, надоело",
]


def _random_birth_date(min_age: int = 20, max_age: int = 55) -> date:
    """Случайная дата рождения в заданном диапазоне возраста."""
    birth_year = date.today().year - random.randint(min_age, max_age)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # до 28, чтобы дата была в любом месяце
    return date(birth_year, month, day)


def _random_username(first_name: str, last_name: str) -> str:
    """Генерирует ник из имени и фамилии, например 'ipetrov' или 'petrov_i'."""
    variants = [
        f"{first_name[0].lower()}{last_name.lower()}",
        f"{last_name.lower()}_{first_name[0].lower()}",
        f"{first_name.lower()}{random.randint(1, 99)}",
        f"{last_name.lower()}{random.randint(10, 999)}",
    ]
    # транслитерация кириллицы (упрощённая)
    translit = {
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d",
        "е": "e", "ё": "e", "ж": "zh", "з": "z", "и": "i",
        "й": "y", "к": "k", "л": "l", "м": "m", "н": "n",
        "о": "o", "п": "p", "р": "r", "с": "s", "т": "t",
        "у": "u", "ф": "f", "х": "kh", "ц": "ts", "ч": "ch",
        "ш": "sh", "щ": "sch", "ъ": "", "ы": "y", "ь": "",
        "э": "e", "ю": "yu", "я": "ya",
    }
    username = random.choice(variants)
    result = ""
    for char in username:
        if char in translit:
            result += translit[char]
        elif char.isascii():
            result += char
    return result


def generate_operator(operator_id: int) -> Operator:
    """Создать случайного оператора."""
    is_male = random.choice([True, False])

    if is_male:
        first_name = random.choice(MALE_FIRST_NAMES)
        patronymic = random.choice(MALE_PATRONYMICS)
        last_name = random.choice(LAST_NAMES_MALE)
    else:
        first_name = random.choice(FEMALE_FIRST_NAMES)
        patronymic = random.choice(FEMALE_PATRONYMICS)
        last_name = random.choice(LAST_NAMES_FEMALE)

    return Operator(
        person_id=operator_id,
        last_name=last_name,
        first_name=first_name,
        patronymic=patronymic,
        city=random.choice(CITIES),
        birth_date=_random_birth_date(22, 45),
        position=random.choice(OPERATOR_POSITIONS),
        experience_years=random.randint(1, 10),
    )


def generate_user(user_id: int) -> User:
    """Создать случайного пользователя."""
    is_male = random.choice([True, False])

    if is_male:
        first_name = random.choice(MALE_FIRST_NAMES)
        patronymic = random.choice(MALE_PATRONYMICS)
        last_name = random.choice(LAST_NAMES_MALE)
    else:
        first_name = random.choice(FEMALE_FIRST_NAMES)
        patronymic = random.choice(FEMALE_PATRONYMICS)
        last_name = random.choice(LAST_NAMES_FEMALE)

    return User(
        person_id=user_id,
        last_name=last_name,
        first_name=first_name,
        patronymic=patronymic,
        city=random.choice(CITIES),
        birth_date=_random_birth_date(18, 55),
        position=random.choice(USER_POSITIONS),
        experience_years=random.randint(0, 20),
        username=_random_username(first_name, last_name),
    )


def random_user_opening() -> str:
    """Случайное первое сообщение от пользователя."""
    return random.choice(USER_OPENING_MESSAGES)


def random_user_followup() -> str:
    """Случайное продолжение диалога от пользователя."""
    # в фразу с {} подставляется номер заказа, остальные не меняются
    return random.choice(USER_FOLLOWUP_MESSAGES).format(random.randint(1000, 9999))


def random_operator_reply() -> str:
    """Случайный ответ оператора."""
    return random.choice(OPERATOR_MESSAGES)


def _later(time: datetime) -> datetime:
    """Время на 1-10 минут позже переданного (следующее сообщение в чате)."""
    return time + timedelta(minutes=random.randint(1, 10))


def populate_platform(platform, n_operators: int = 15, n_users: int = 50):
    """Заполнить платформу случайными операторами и пользователями."""
    for i in range(1, n_operators + 1):
        platform.register_operator(generate_operator(i))

    for i in range(1, n_users + 1):
        platform.register_user(generate_user(i))


def simulate_chats(platform, n_chats: int = 120):
    """
    Создать n_chats чатов с сообщениями и разными статусами.

    Примерное распределение:
    ~60% - закрытые с оценкой CSAT
    ~20% - закрытые без CSAT
    ~20% - открытые (в процессе)
    На деле открытых получается меньше: когда свободных операторов нет,
    один из открытых чатов закрывается.
    """
    created = 0

    # время симуляции: начинаем в прошлом и двигаемся вперёд,
    # новый чат - через 1-60 минут после предыдущего
    clock = datetime.now() - timedelta(minutes=30 * n_chats)

    for _ in range(n_chats):
        clock += timedelta(minutes=random.randint(1, 60))
        user = random.choice(platform.users)

        # если нет свободных операторов - закрываем случайный открытый чат,
        # чтобы освободить оператора
        if not platform.get_available_operators():
            open_chats = [c for c in platform.chats if c.status == "open"]
            if open_chats:
                chat_to_close = random.choice(open_chats)
                # закрываем не раньше последнего сообщения в этом чате
                close_time = chat_to_close.messages[-1].timestamp + timedelta(minutes=1)
                if close_time < clock:
                    close_time = clock
                chat_to_close.close(close_time)
                if random.random() < 0.75:
                    chat_to_close.set_csat(random.randint(1, 5))
            else:
                continue

        chat = platform.create_chat(user, created_at=clock)
        created += 1

        time = _later(clock)
        chat.send_user_message(random_user_opening(), time)

        # диалог: 1-4 пары сообщений (оператор-пользователь)
        n_exchanges = random.randint(1, 4)
        for _ in range(n_exchanges):
            time = _later(time)
            chat.send_operator_message(random_operator_reply(), time)
            # пользователь не всегда отвечает
            if random.random() < 0.8:
                time = _later(time)
                chat.send_user_message(random_user_followup(), time)

        # 60% - закрыт с CSAT, 20% - закрыт без CSAT, 20% - остаётся открытым
        roll = random.random()
        if roll < 0.6:
            chat.close(_later(time))
            chat.set_csat(random.randint(1, 5))
        elif roll < 0.8:
            chat.close(_later(time))

    return created
