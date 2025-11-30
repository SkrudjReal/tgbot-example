from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.utils import callback_data as cd


def _example_inline_kb():
    kb = InlineKeyboardBuilder()
    
    kb.button(text='Example', callback_data=cd._ExampleCallback(action='example'))
    
    kb.adjust(1)
    return kb.as_markup()
