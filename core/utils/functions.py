from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import StartMode, DialogManager

from core.utils.aio_dialogs_widgets import DialogSG

import re


async def send_scrolling_text_dialog(
    dialog_manager: DialogManager,
    text: str,
    start_mode: StartMode = StartMode.NEW_STACK
):
    await dialog_manager.start(
        DialogSG.TEXT,
        mode=start_mode,
        data={"operations_text": text}
    )

def is_float(s: str) -> bool:
    return bool(re.fullmatch(r'[+-]?\d+(\.\d+)?', s))

def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False
