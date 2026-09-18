# Модели данных платформы поддержки

from support_platform.models.person import Person
from support_platform.models.operator import Operator
from support_platform.models.user import User
from support_platform.models.message import Message
from support_platform.models.chat import Chat

__all__ = ["Person", "Operator", "User", "Message", "Chat"]
