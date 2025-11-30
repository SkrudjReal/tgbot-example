from aiogram.utils.keyboard import ReplyKeyboardBuilder


def _example_kb():
    kb = ReplyKeyboardBuilder()
    
    kb.button(text='example')
    
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

