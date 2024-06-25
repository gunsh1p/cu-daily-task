from datetime import datetime

from aiogram import Dispatcher, F, Router
from aiogram.types import CallbackQuery
from tortoise.exceptions import DoesNotExist

from db.models import Event
from keyboards.events import get_events_kb
from keyboards.event import get_event_kb

router = Router(name="user-start")


@router.callback_query(F.data.startswith('event:'))
async def event_callback(callback: CallbackQuery):
    await callback.answer()
    event_id = int(callback.data.split(":")[1])
    try:
        event = await Event.get(id=event_id)
    except DoesNotExist:
        return
    t = (datetime.min + event.time).time()
    t = t.strftime('%H:%M')
    text = (
        f'Название: {event.title}\n'
        f'Время: {t}\n'
        f'Chat ID: {event.chat_id}'
    )
    await callback.message.edit_text(
        text=text,
        reply_markup=get_event_kb(event),
    )


@router.callback_query(F.data.startswith('delete:'))
async def delete_callback(callback: CallbackQuery):
    await callback.answer()
    event_id = int(callback.data.split(":")[1])
    event = await Event.get_or_none(id=event_id)
    if event:
        await event.delete()
    events = await Event.all()
    await callback.message.edit_text(
        text='Событие удалено\nСписок доступных событий',
        reply_markup=get_events_kb(events)
    )


def register_router(dp: Dispatcher):
    dp.include_router(router)
