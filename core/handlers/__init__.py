from aiogram import Router, F, Dispatcher

from .start import router as start_router


def setup_routers(dp: Dispatcher):
    dp.include_routers(start_router)