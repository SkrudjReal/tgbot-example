from aiogram import BaseMiddleware
from aiogram.types import Update
from cachetools import TTLCache
from typing import Awaitable, Callable, Dict, Any


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: float=1.5)-> None:
        self.rate_limit = TTLCache(maxsize=10_000, ttl=limit)

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        user = data.get('event_from_user')
        
        if not user:
            return await handler(event, data)
        
        if user.id in self.rate_limit:
            return

        self.rate_limit[user.id] = None

        return await handler(event, data)

