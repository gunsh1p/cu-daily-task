import asyncio

from aiogram import Bot
import aioschedule

from .notify import notify_daily


async def register(bot: Bot):
    aioschedule.every(1).minutes.do(notify_daily, bot=bot)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
