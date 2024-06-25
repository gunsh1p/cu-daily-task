from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_cancel_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отменить", callback_data="cancel")]
        ]
    )
    return kb
