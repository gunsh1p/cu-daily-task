from aiogram import Dispatcher, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from db.models import Event
from keyboards.events import get_events_kb

router = Router(name="user-start")


@router.message(Command("start"))
async def start_command(message: Message):
    events = await Event.all()
    await message.answer(
        text="Список доступных событий", reply_markup=get_events_kb(events)
    )


@router.callback_query(F.data.in_(["cancel", "menu"]))
async def cancel_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    events = await Event.all()
    text = "Действия отменены\nСписок доступных событий" if callback.data == "cancel" else "Список доступных событий"
    await callback.message.edit_text(
        text=text,
        reply_markup=get_events_kb(events),
    )


def register_router(dp: Dispatcher):
    dp.include_router(router)
