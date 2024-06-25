from datetime import datetime, timedelta
import pytz

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from db.models import Event
from utils.leetcode import get_daily


async def notify_daily(bot: Bot):
    daily_task = await get_daily()
    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Решать", url=daily_task)]]
    )
    now = datetime.now(tz=pytz.UTC)
    async for event in Event.all():
        if event.next_run > now:
            continue

        try:
            await bot.send_message(
                text="Решаем сегодняшний дейлик",
                reply_markup=kb,
                chat_id=event.chat_id,
                message_thread_id=event.thread_id,
            )
        except Exception:
            continue

        event.next_run += timedelta(days=1)
        await event.save()
