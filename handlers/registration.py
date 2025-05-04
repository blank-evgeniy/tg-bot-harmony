from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command

from services.airtable import airtable
from states.registration_states import RegistrationStates
from keyboards.enter_phone_kb import enter_phone_kb
from keyboards.main_menu_kb import main_menu_kb

router = Router()


@router.callback_query(F.data == "share_phone")
async def request_phone(callback: types.CallbackQuery, state: FSMContext):
  await callback.message.answer(
        "Нажмите кнопку ниже чтобы автоматически отправить телефон:",
        reply_markup=enter_phone_kb()
    )
  await callback.answer()

@router.message(RegistrationStates.waiting_for_phone, F.contact | (F.text.regexp(r'^\+?[0-9\s\-\(\)]{10,}$')))
async def handle_phone_input(message: types.Message, state: FSMContext):
  if message.contact:
      if message.contact.user_id != message.from_user.id:
          await message.answer("Пожалуйста, отправьте свой контакт")
          return
      phone = message.contact.phone_number
  else:
      phone = message.text

  await state.update_data(phone=phone)
  await state.set_state(RegistrationStates.waiting_for_name)
  await message.answer("Отлично! Теперь введите ваше имя:", reply_markup=types.ReplyKeyboardRemove())

@router.message(RegistrationStates.waiting_for_phone)
async def handle_phone_input_error(message: types.Message):
    await message.answer("Пожалуйста, введите ваш номер телефона.")

@router.message(RegistrationStates.waiting_for_name, F.text.len() >= 2)
async def handle_name_input(message: types.Message, state: FSMContext):
    data = await state.get_data()

    record = await airtable.create_client(message.from_user.id, message.text, data["phone"])
    await state.clear()

    if record:
      await message.answer(
          f"Спасибо, {message.text}! Теперь вы можете записаться на услугу.",
          reply_markup=main_menu_kb()
      )
    else:
       await message.answer(
          f"Произошла ошибка. Пожалуйста, попробуйте позже.",
          reply_markup=main_menu_kb()
      )

@router.message(RegistrationStates.waiting_for_name)
async def handle_name_input_error(message: types.Message):
    await message.answer("Пожалуйста, введите ваше имя (не менее 2 символов).")

@router.message(
    StateFilter(RegistrationStates),
    F.text == "❌ Отмена"
)
@router.message(
    StateFilter(RegistrationStates),
    Command(commands=["cancel"])
)
async def handle_cancel_during_registration(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "❌ Регистрация отменена",
        reply_markup=main_menu_kb()
    )   