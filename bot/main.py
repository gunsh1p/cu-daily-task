import asyncio
import logging
import sys

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from tortoise import Tortoise

from config import config
from handlers import start, create, event
from middlewares.admin import IsAdminMiddleware
import tasks
from db.config import CONFIG_ORM

storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dbp = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(config.BOT_TOKEN, default=dbp)


async def on_startup(bot: Bot):
    await bot.delete_webhook()


async def setup_handlers():
    start.register_router(dp)
    create.register_router(dp)
    event.register_router(dp)


async def setup_middlewares():
    dp.message.middleware(IsAdminMiddleware())
    dp.callback_query.middleware(IsAdminMiddleware())


async def main():
    await Tortoise.init(CONFIG_ORM)
    asyncio.create_task(tasks.register(bot))
    await setup_handlers()
    await setup_middlewares()
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="[%(asctime)s] %(levelname)s:%(name)s: %(message)s",
    )
    asyncio.run(main())
