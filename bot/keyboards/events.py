from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.models import Event
from utils.truncate_string import truncate_string


def get_events_kb(events: list[Event]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if len(events) > 0:
        for event in events:
            builder.row(
                InlineKeyboardButton(
                    text=truncate_string(event.title),
                    callback_data=f"event:{event.id}"
                )
            )
    else:
        builder.row(
            InlineKeyboardButton(
                text='Событий нет :(',
                callback_data='none'
            )
        )
    builder.row(
        InlineKeyboardButton(
            text='Создать событие',
            callback_data='create_event'
        )
    )
    return builder.as_markup()
