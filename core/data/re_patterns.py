from __future__ import annotations

from typing import Final
from aiogram import html

import re

class UserPattern:
    
    USER_LINK = re.compile(
        r'(?:https?://t\.me/|tg://openmessage\?user_id=|@)(\d{6,16}|[\w\d]{4,32})',
        re.IGNORECASE
    )
    
    @staticmethod
    def get_mention(part_text: str) -> str | int | None:
        pattern = re.search(UserPattern.USER_LINK, part_text)
        return (int(pattern.group(1)) if pattern.group(1).isdigit() else pattern.group(1)) if pattern else None


user_pattern = UserPattern