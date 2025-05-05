from aiogram.types import CallbackQuery
from aiogram import Router, F
from keyboards.categories_kb import categories_kb
from services.airtable import airtable
from services.airtable import airtable

router = Router()


@router.callback_query(F.data.startswith("category_"))
async def handle_category_selection(callback: CallbackQuery):
    category = callback.data.split("_")[1]
    records = await airtable.get_procedures_by_category(category)
    # отобразить инлайн клаву - список процедур

    await callback.answer()

# Обработчик возврата
@router.callback_query(F.data == "back_to_categories")
async def back_to_categories(callback: CallbackQuery):
    categories = await airtable.get_categories()

    await callback.message.edit_text(
        "Выберите категорию:",
        reply_markup=categories_kb(categories)
    )
    await callback.answer()