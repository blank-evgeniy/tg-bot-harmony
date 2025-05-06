from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from keyboards.categories_kb import categories_kb
from keyboards.procedures_kb import procedures_kb
from keyboards.days_kb import days_kb
from services.airtable import airtable
from states.booking_states import BookingStates

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

    await callback.message.edit_text(
        "Выберите категорию:",
        reply_markup=categories_kb(categories)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("procedure_"))
async def handle_procedure_selection(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category_name = data.get('current_category_name', 'Неизвестная категория')

    data = await airtable.get_category_days(category_name)

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
    
    procedures = await airtable.get_procedures_by_category(category_name)

    await callback.message.edit_text("Выберите процедуру:", reply_markup=procedures_kb(procedures))
    await callback.answer()