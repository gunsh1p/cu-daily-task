from datetime import timedelta, time, datetime, date

from aiogram import Dispatcher, Bot, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from db.models import Event
from keyboards.cancel import get_cancel_kb
from keyboards.create import get_skip_kb
from keyboards.event import get_event_kb
from states import CreateEvent

router = Router(name="user-create")


@router.callback_query(F.data == "create_event")
async def create_event_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    msg_id = callback.message.message_id
    await callback.message.edit_text(
        text="Введите название события (до 50 символов):", reply_markup=get_cancel_kb()
    )
    await state.update_data(msg_id=msg_id)
    await state.set_state(CreateEvent.title)


@router.message(CreateEvent.title)
async def title_message(message: Message, state: FSMContext, bot: Bot):
    await message.delete()
    data = await state.get_data()
    msg_id = data["msg_id"]
    title = message.text.strip()[:50]

    await bot.edit_message_text(
        text="Введите время в формате hh:mm (например, 10:00):",
        reply_markup=get_cancel_kb(),
        chat_id=message.from_user.id,
        message_id=msg_id,
    )
    await state.update_data(title=title)
    await state.set_state(CreateEvent.time)


@router.message(CreateEvent.time)
async def time_message(message: Message, state: FSMContext, bot: Bot):
    await message.delete()
    data = await state.get_data()
    msg_id = data["msg_id"]
    t = message.text.strip() + ':00'

    try:
        t = time.fromisoformat(t)
    except Exception:
        await bot.edit_message_text(
            text="Неверный формат. Введите время в формате hh:mm (например, 10:00):",
            reply_markup=get_cancel_kb(),
            chat_id=message.from_user.id,
            message_id=msg_id,
        )
        return

    await bot.edit_message_text(
        text="Введите chat id:",
        reply_markup=get_cancel_kb(),
        chat_id=message.from_user.id,
        message_id=msg_id,
    )
    await state.update_data(time=t)
    await state.set_state(CreateEvent.chat_id)


@router.message(CreateEvent.chat_id)
async def chat_id_message(message: Message, state: FSMContext, bot: Bot):
    await message.delete()
    data = await state.get_data()
    msg_id = data["msg_id"]
    cid = message.text.strip()

    try:
        cid = int(cid)
    except Exception:
        await bot.edit_message_text(
            text="Неверный формат. Введите chat id:",
            reply_markup=get_cancel_kb(),
            chat_id=message.from_user.id,
            message_id=msg_id,
        )
        return

    await bot.edit_message_text(
        text="Введите thread id (если требуется):",
        reply_markup=get_skip_kb(),
        chat_id=message.from_user.id,
        message_id=msg_id,
    )
    await state.update_data(cid=cid)
    await state.set_state(CreateEvent.thread_id)


@router.callback_query(CreateEvent.thread_id, F.data == 'skip')
async def thread_id_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    title = data["title"]
    t = data["time"]
    cid = data["cid"]
    tid = None

    dt = datetime.combine(date.today(), t) - timedelta(hours=3)
    event = await Event.create(title=title, time=t, next_run=dt, chat_id=cid, thread_id=tid)
    t = t.strftime('%H:%M')
    text = (
        f'Название: {title}\n'
        f'Время: {t}\n'
        f'Chat ID: {cid}'
    )
    await callback.message.edit_text(
        text=text,
        reply_markup=get_event_kb(event)
    )

@router.message(CreateEvent.thread_id)
async def thread_id_message(message: Message, state: FSMContext, bot: Bot):
    await message.delete()
    data = await state.get_data()
    msg_id = data["msg_id"]
    title = data["title"]
    t = data["t"]
    cid = data["cid"]
    tid = message.text.strip()

    try:
        tid = int(tid)
    except Exception:
        await bot.edit_message_text(
            text="Неверный формат. Введите thread id (если требуется):",
            reply_markup=get_cancel_kb(),
            chat_id=message.from_user.id,
            message_id=msg_id,
        )
        return

    dt = datetime.combine(date.today(), t) - timedelta(hours=3)
    event = await Event.create(title=title, time=t, next_run=dt, chat_id=cid, thread_id=tid)
    t = t.strftime('%H:%M')
    text = (
        f'Название: {title}\n'
        f'Время: {t}\n'
        f'Chat ID: {cid}'
    )
    await bot.edit_message_text(
        text=text,
        reply_markup=get_event_kb(event),
        chat_id=message.from_user.id,
        message_id=msg_id,
    )


def register_router(dp: Dispatcher):
    dp.include_router(router)
