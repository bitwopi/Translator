import asyncio
import logging
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.set_bot_commands import set_default_commands
from bot.handlers.user_handlers import register_user_handlers

logger = logging.getLogger(__name__)

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)


def register_all_handlers(dp):
    register_user_handlers(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    token = os.getenv('API_TOKEN')
    bot = Bot(token=token)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    register_all_handlers(dp)
    await set_default_commands(bot)

    # start
    try:
        await dp.start_polling()
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
