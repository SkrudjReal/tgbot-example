from asyncmy.cursors import DictCursor
from asyncmy.pool import Pool
from redis.asyncio import Redis

from aiogram import BaseMiddleware, Bot
from aiogram.types import Update
from aiogram import html

from typing import Awaitable, Callable, Dict, Any

from core.utils.db_api.repo import RequestsRepo


class DBPoolMiddleware(BaseMiddleware):

    def __init__(self, pool: Pool, redis: Redis, bot: Bot) -> None:
        self.pool: Pool = pool
        self.redis: Redis = redis
        self.bot: Bot = bot

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        
        if event.pre_checkout_query:
            return await handler(event, data)
        
        async with self.pool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                repo = RequestsRepo(cur)
                user = data.get('event_from_user')
                # chat = data.get('event_chat')
                # message = data.get('event_update')
                
                await repo.add_data_user(
                    user.id,
                    html.quote(user.full_name),
                    user.username
                )
                data['redis'] = self.redis
                data['db'] = cur
                data['repo'] = repo
                
                return await handler(event, data)


