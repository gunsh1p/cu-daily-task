from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_skip_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Пропустить", callback_data="skip")],
            [InlineKeyboardButton(text="Отменить", callback_data="cancel")]
        ]
    )
    return kb
