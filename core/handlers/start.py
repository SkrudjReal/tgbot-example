from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router, F

from core.utils.db_api.repo import RequestsRepo

import time


router = Router()

@router.message(CommandStart())
async def start_handler(msg: Message, repo: RequestsRepo):
    
    user_info = await repo.get_user(msg.from_user.id)
    
    await msg.answer(
        f'👋 Привет, <b>{msg.from_user.full_name}</b>!\n'
        'Я — твой бот. Доступные команды: /help, пинг.\n\n'
        f'Вот что я знаю о тебе: {user_info}'
    )

@router.message(F.text == 'пинг')
async def ping(msg: Message):
    time_start = time.time()
    mesg = await msg.answer('🏓 Понг!')
    time_end = time.time()
    await mesg.edit_text(f'🏓 Понг!\nСкорость ответа бота секунд: {time_end-time_start:.3f}')

