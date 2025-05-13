from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from keyboards.categories_kb import categories_kb
from keyboards.procedures_kb import procedures_kb
from keyboards.days_kb import days_kb
from keyboards.times_kb import times_kb
from services.airtable import airtable
from states.booking_states import BookingStates
from lib.formatters import format_seconds_to_time

router = Router()


@router.callback_query(F.data.startswith("category_"))
async def handle_category_selection(callback: CallbackQuery, state: FSMContext):
    category_id = callback.data.split("_")[1]
    category_name = await airtable.get_category_name(category_id)

    await state.update_data(
        current_category_id=category_id,
        current_category_name=category_name
    )

    await state.set_state(BookingStates.waiting_for_procedure)

    procedures = await airtable.get_procedures_by_category(category_name)

    await callback.message.edit_text("Выберите процедуру:", reply_markup=procedures_kb(procedures))
    await callback.answer()

# Обработчик возврата
@router.callback_query(F.data == "back_to_categories")
async def back_to_categories(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    categories = await airtable.get_categories()

    await state.set_state(BookingStates.waiting_for_procedure)

    await callback.message.edit_text(
        "Выберите категорию:",
        reply_markup=categories_kb(categories)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("procedure_"))
async def handle_procedure_selection(callback: CallbackQuery, state: FSMContext):
    procedure_id = callback.data.split("_")[1]

    data = await state.get_data()
    category_name = data.get('current_category_name', 'Неизвестная категория')

    data = await airtable.get_category_days(category_name)

    await state.set_state(BookingStates.waiting_for_date)
    await state.update_data(
        current_category_dates=data,
        current_procedure_id=procedure_id
    )

    if len(data):
        unique_dates = {entry['fields']['Дата'] for entry in data}
        unique_dates_list = list(unique_dates)

        await callback.message.edit_text(
        "Выберите дату:",
        reply_markup=days_kb(unique_dates_list)
    )


    await callback.answer()

@router.callback_query(F.data == "back_to_procedures")
async def back_to_procedures(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category_name = data.get('current_category_name', 'Неизвестная категория')

    await state.set_state(BookingStates.waiting_for_procedure)
    
    procedures = await airtable.get_procedures_by_category(category_name)

    await callback.message.edit_text("Выберите процедуру:", reply_markup=procedures_kb(procedures))
    await callback.answer()

@router.callback_query(F.data.startswith("date_"))
async def handle_date_selection(callback: CallbackQuery, state: FSMContext):
    selected_date = callback.data.split("_")[1]
    
    data = await state.get_data()
    dates = data.get('current_category_dates', 'Неизвестная дата')


    await state.set_state(BookingStates.waiting_for_time)
    await state.update_data(
        current_selected_date=selected_date
    )

    if len(dates):
        await callback.message.edit_text(
        "Выберите время:",
        reply_markup=times_kb(dates)
    )


    await callback.answer()

@router.callback_query(F.data == "back_to_dates")
async def back_to_dates(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    dates = data.get('current_category_dates', 'Неизвестная дата')

    await state.set_state(BookingStates.waiting_for_date)
    
    if len(dates):
        unique_dates = {entry['fields']['Дата'] for entry in dates}
        unique_dates_list = list(unique_dates)

        await callback.message.edit_text(
        "Выберите дату:",
        reply_markup=days_kb(unique_dates_list)
    )

    await callback.answer()

@router.callback_query(F.data.startswith("time_"))
async def handle_date_selection(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    selected_date = data.get('current_selected_date')
    start_time = callback.data.split("_")[1]
    end_time = callback.data.split("_")[2]
    procedure_id = data.get('current_procedure_id')
    procedure_data = await airtable.get_procedure_data(procedure_id)

    print(start_time, end_time)

    # произвести запись в БД

    message = (
        "Вы успешно записались на услугу!\n"
        f"Услуга: {procedure_data['fields']['Название']}\n"
        f"Дата: {selected_date}\n"
        f"Время: {format_seconds_to_time(start_time)} - {format_seconds_to_time(end_time)}\n"
        f"Стоимость: {procedure_data['fields']['Стоимость']}₽"
    )

    await callback.message.edit_text(
        message
    )

    state.clear()
    callback.answer()
