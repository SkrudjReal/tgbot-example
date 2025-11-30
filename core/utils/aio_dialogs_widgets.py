import re

from aiogram.fsm.state import State, StatesGroup

from aiogram_dialog.widgets.text import ScrollingText


from aiogram_dialog import (
    Dialog,
    Window,
    DialogManager
)
from aiogram_dialog.widgets.kbd import (
    Row,
    PrevPage,
    FirstPage,
    NextPage,
    LastPage,
    CurrentPage
)
from aiogram_dialog.widgets.text import (
    ScrollingText,
    Format
)
from aiogram_dialog.widgets.link_preview import LinkPreview


class WordScrollingText(ScrollingText):
    def _split_text_by_words(self, text: str) -> list[str]:
        return re.findall(r'.*(?:\n|$)', text)

    def _split_to_pages(self, text: str) -> list[str]:
        words = self._split_text_by_words(text)
        pages = []
        current_page = ""
        for word in words:
            if len(current_page) + len(word) > self.page_size:
                if current_page:
                    pages.append(current_page.rstrip())
                    current_page = word
                else:
                    pages.append(word.rstrip())
                    current_page = ""
            else:
                current_page += word
        if current_page:
            pages.append(current_page.rstrip())
        return pages

    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        full_text = await self._render_contents(data, manager)
        pages = self._split_to_pages(full_text)
        page = await self.get_page(manager)
        return pages[min(page, len(pages) - 1)]

    async def get_page_count(self, data: dict, manager: DialogManager) -> int:
        full_text = await self._render_contents(data, manager)
        return len(self._split_to_pages(full_text))

class DialogSG(StatesGroup):
    TEXT = State()

dialog = Dialog(
    Window(
        LinkPreview(is_disabled=True),
        WordScrollingText(
            text=Format("{start_data[operations_text]}"),
            id="text_scroll",
            page_size=2048
        ),
        Row(
            FirstPage(scroll="text_scroll", text=Format("⏮️")),
            PrevPage(scroll="text_scroll", text=Format("◀️")),
            CurrentPage(scroll="text_scroll"),
            NextPage(scroll="text_scroll", text=Format("▶️")),
            LastPage(scroll="text_scroll", text=Format("⏭️"))
        ),
        state=DialogSG.TEXT,
    ),
)