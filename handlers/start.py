from aiogram import types, Router, F
from aiogram.filters import Command
from keyboards.main_menu_kb import main_menu_kb
from keyboards.request_contact_kb import request_contact_kb
from keyboards.categories_kb import categories_kb
from services.airtable import airtable
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from states.registration_states import RegistrationStates

router = Router()

@router.message(Command("start"))
async def command_start(message: types.Message) -> None:
    """Обработчик команды /start"""

    welcome_message = (
    '💖 <b>{Name}, добро пожаловать в салон красоты!</b> 💖\n\n'
    'Если хотите записаться на услугу онлайн, выберите в нижнем меню соответствующее действие.\n\n'
    "<i>Мы не просто создаем образы — мы раскрываем вашу природную красоту и дарим неповторимые эмоции!</i> 💫"
    )

    photo_path = "images/welcome.jpg"
    photo = FSInputFile(photo_path)

    await message.answer_photo(photo=photo, caption=welcome_message.format(Name=message.from_user.first_name), reply_markup=main_menu_kb())

@router.message(F.text == "📅 Записаться")
async def booking_handle(message: types.Message, state: FSMContext):
    """Обработчик команды '📅 Записаться'"""

    has_client = await airtable.check_user_exists(message.from_user.id)

    if (has_client):
        categories = await airtable.get_categories()
        keyboard = categories_kb(categories)

        await message.answer("Выберите категорию:", reply_markup=keyboard)
    else:
        await message.answer("Для записи нам нужны ваши данные.\n", reply_markup=request_contact_kb())
        await state.set_state(RegistrationStates.waiting_for_phone)

@router.message(F.text == "📞 Контакты")
async def contacts_handle(message: types.Message):
    """Обработчик команды '📞 Контакты'"""

    contact_text = (
        "<b>🌸 Наши контакты:</b>\n\n"
        "📍 <b>Адрес:</b> г. Калининград, ул. Красивая, 15\n"
        "📞 <b>Телефоны:</b>\n"
        "+7 (495) 123-45-67\n"
        "+7 (977) 765-43-21 (WhatsApp)\n\n"
        "🕒 <b>Часы работы:</b>\n"
        "Пн-Вс: 10:00 - 21:00"
    )

    photo_path = "images/contacts.jpg"
    photo = FSInputFile(photo_path)

    await message.answer_photo(photo=photo, caption=contact_text)

@router.message(Command("reminder2"))
async def command_start(message: types.Message) -> None:
    """Обработчик команды /reminder2"""

    message_text = (
    '<b>Анастасия, скоро увидимся!</b> ✨ \n'
    'Через 2 часа у вас запись на услугу "Стрижка". Пожалуйста, не опаздывайте.\n\n'
    )

    await message.answer(message_text.format(Name=message.from_user.first_name), reply_markup=main_menu_kb())

@router.message(Command("reminder24"))
async def command_start(message: types.Message) -> None:
    """Обработчик команды /reminder24"""

    message_text = (
    '<b>Привет, Анастасия!</b> ☺️\n'
    ' Завтра в 13:00 у вас запись на услугу "Стрижка". Не забудьте заглянуть к нам. До встречи!\n\n'
    )

    await message.answer(message_text.format(Name=message.from_user.first_name), reply_markup=main_menu_kb())