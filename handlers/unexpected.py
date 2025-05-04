from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_menu_kb import main_menu_kb

router = Router()

@router.message()
async def handle_unexpected(message: Message):
    """Ловит все сообщения, не обработанные другими хэндлерами"""
    await message.answer(
        "⚠️ Я не понимаю эту команду. Пожалуйста, используйте меню:",
        reply_markup=main_menu_kb()
    )