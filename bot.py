import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message

from config import TG_TOKEN
from handlers.start import command_start_handler

# Логирование
logging.basicConfig(level=logging.INFO)

# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(CommandStart())
async def handle_command_start(message: Message):
    await command_start_handler(message)

# Запуск процесса поллинга новых апдейтов
async def main():
    bot = Bot(token=TG_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())