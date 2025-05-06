from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def categories_kb(categories_data):
    builder = InlineKeyboardBuilder()
    
    for category in categories_data:
        category_name = category['fields']['Название']
        category_id = category['id']

        builder.add(InlineKeyboardButton(
            text=category_name,
            callback_data=f"category_{category_id}"
        ))

    builder.adjust(2)
    return builder.as_markup()