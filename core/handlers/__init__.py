from aiogram import Router, F, Dispatcher

from core.utils import aio_dialogs_widgets

from . import start


def setup_routers(dp: Dispatcher):
    routers = [
        aio_dialogs_widgets.dialog,
        start.router,
    ]
    
    dp.include_routers(*routers)

