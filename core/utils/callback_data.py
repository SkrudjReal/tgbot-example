from aiogram.filters.callback_data import CallbackData


class _ExampleCallback(CallbackData, prefix="ec"):
    action: str

