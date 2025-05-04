import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import TG_TOKEN
from handlers import registration, start, unexpected

# Логирование
logging.basicConfig(level=logging.INFO)

# Запуск процесса поллинга новых апдейтов
async def main():
    bot = Bot(token=TG_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start.router)
    dp.include_router(registration.router)
    dp.include_router(unexpected.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())