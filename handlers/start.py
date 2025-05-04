from aiogram import types, Router, F
from aiogram.filters import Command
from keyboards.main_menu_kb import main_menu_kb

router = Router()

@router.message(Command("start"))
async def command_start(message: types.Message) -> None:
    """Обработчик команды /start"""

    welcome_message = (
    '💖 <b>{Name}, добро пожаловать в салон красоты "Harmony"!</b> 💖\n\n'
    "<i>Мы не просто создаем образы — мы раскрываем вашу природную красоту и дарим неповторимые эмоции!</i> 💫"
    )

    await message.answer(welcome_message.format(Name=message.from_user.first_name), reply_markup=main_menu_kb())

@router.message(F.text == "📅 Записаться")
async def answer_yes(message: types.Message):
    await message.answer(
        "Выберите категорию услуг:",
    )

@router.message(F.text == "📞 Контакты")
async def answer_yes(message: types.Message):
    contact_text = (
        "<b>🌸 Наши контакты:</b>\n\n"
        "📍 <b>Адрес:</b> г. Калининград, ул. Красивая, 15\n"
        "📞 <b>Телефоны:</b>\n"
        "+7 (495) 123-45-67\n"
        "+7 (977) 765-43-21 (WhatsApp)\n\n"
        "🕒 <b>Часы работы:</b>\n"
        "Пн-Вс: 10:00 - 21:00"
    )

    await message.answer(contact_text)