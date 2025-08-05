from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from asyncmy.pool import Pool
from redis.asyncio import Redis

from core.utils.db_api.create_database import create_pool, db_setup
from core.utils.commands import set_commands, del_commands
from core.middlewares import DBPoolMiddleware, ThrottlingMiddleware
from core.service.loop_task import scheduler_tasks
from core.settings import settings, logger
from core.handlers import setup_routers

import asyncio
import uvloop
import os


async def on_startup(bot: Bot):
    me = await bot.get_me()
    logger.info(f'Бот @{me.username} [{me.id}] - PID {os.getpid()} запущен.')

async def setup_middlewares(dp: Dispatcher, pool: Pool, redis: Redis, bot: Bot):
    dp.update.outer_middleware.register(DBPoolMiddleware(pool, redis, bot))
    dp.message.middleware.register(ThrottlingMiddleware(limit=1.5))

async def main():
    
    bot = Bot(token=settings.bot.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    pool = await create_pool()
    redis = Redis(host=settings.redis.ip, port=6379, decode_responses=True)
    scheduler = AsyncIOScheduler()
    
    await db_setup(pool)
    await setup_middlewares(dp, pool, redis, bot)
    setup_routers(dp)
    
    await del_commands(bot)
    await set_commands(bot)
    
    await scheduler_tasks(pool, bot, scheduler)
    
    try:
        logger.info("Стартуем polling...")
        scheduler.start()
        await on_startup(bot)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.exception(f"Ошибка при запуске: {e}")
    finally:
        scheduler.shutdown()
        await bot.session.close()
        logger.info('Бот остановлен.')
    

if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(main())