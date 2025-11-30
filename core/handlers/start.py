from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from aiogram_dialog import DialogManager

from core.utils.db_api.repo import RequestsRepo
from core.utils import functions
from core.data import messages, links

import time


router = Router()

@router.message(CommandStart())
async def start_handler(msg: Message, repo: RequestsRepo, dialog_manager: DialogManager, state: FSMContext):
    
    # Clear FSM and Dialog Manager stack
    await dialog_manager.reset_stack()
    await state.clear()
    
    user_info = await repo.get_user(msg.from_user.id)
    user = msg.from_user
    
    mention = links.user_mention(user.id, user.full_name)
    text = messages['start']['_welcome_text'].format(
        mention=mention,
        user_id=user_info['user_id'],
        full_name=user_info['full_name'],
        username=user_info['username'] if user_info['username'] else ''
    )
    
    await functions.send_scrolling_text_dialog(dialog_manager, text)

@router.message(F.text == 'пинг')
async def ping(msg: Message):
    time_start = time.time()
    mesg = await msg.answer('🏓 Понг!')
    time_end = time.time()
    await mesg.edit_text(f'🏓 Понг!\nСкорость ответа бота секунд: {time_end-time_start:.3f}')

