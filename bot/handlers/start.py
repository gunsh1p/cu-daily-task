from aiogram import Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command

from db.models import Event
from keyboards.events import get_events_kb

router = Router(name="user-start")

@router.message(
    Command("start")
)
async def start_command(message: Message):
    events = await Event.all()
    await message.delete()
    await message.answer(
        text='Список доступных событий',
        reply_markup=get_events_kb(events)
    )

def register_router(dp: Dispatcher):
    dp.include_router(router)