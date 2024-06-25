from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from db.models import Event

def get_event_kb(event: Event) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Удалить", callback_data=f"delete:{event.id}")],
            [InlineKeyboardButton(text="Меню", callback_data="menu")]
        ]
    )
    return kb
