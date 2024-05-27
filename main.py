import asyncio
import locale
import logging
import os

import vk_api
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from dotenv import load_dotenv, find_dotenv
from redis.asyncio import Redis

from src.database.engine import session_maker
from src.dialogs import dialog_router
from src.handlers.admin_private import admin_router
from src.handlers.user_group import user_group_router
from src.handlers.user_private import user_private_router
from src.middlewares.db import DataBaseSession

load_dotenv(find_dotenv())

locale.setlocale(locale.LC_ALL, "")

bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
redis = Redis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
)
storage = RedisStorage(redis=redis, key_builder=DefaultKeyBuilder(with_destiny=True))

# Авторизация в Вконтакте
vk_session = vk_api.VkApi(
    token=os.getenv('VK_TOKEN'))
vk = vk_session.get_api()


async def on_startup(bot):
    # await drop_db()

    from src.database.engine import create_db
    await create_db()


async def on_shutdown(bot):
    print('бот лег')


def setup_dp():
    dp = Dispatcher(storage=storage, events_isolation=SimpleEventIsolation())
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    dp.include_router(user_private_router)
    dp.include_router(user_group_router)
    dp.include_router(admin_router)
    dp.include_router(dialog_router)
    setup_dialogs(dp)
    return dp


async def main():
    logging.basicConfig(level=logging.INFO)
    dp = setup_dp()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
