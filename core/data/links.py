from __future__ import annotations

from typing import Final
from aiogram import html


class DeepLink:
    
    # Обычные ссылки
    TAG: Final[str] = "@"
    
    # Дип-линки Telegram
    OPEN_MESSAGE: Final[str] = "tg://openmessage?user_id="      # MENTION создает вечную ссылку
    USER_PROFILE: Final[str] = "tg://user?id="                  # TAG тегает юзера
    
    # Удобные методы
    @staticmethod
    def user_mention(user_id: int, name: str) -> str:
        return f"<a href='{DeepLink.OPEN_MESSAGE}{user_id}'>{html.quote(name)}</a>"

    @staticmethod
    def user_profile(user_id: int, name: str) -> str:
        return f"<a href='{DeepLink.USER_PROFILE}{user_id}'>{html.quote(name)}</a>"

    @staticmethod
    def username_tag(username: str) -> str:
        return f"{DeepLink.TAG}{username.lstrip('@')}"


links = DeepLink