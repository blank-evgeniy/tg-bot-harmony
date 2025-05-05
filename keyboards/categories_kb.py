from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def categories_kb(categories_data):
    builder = InlineKeyboardBuilder()

    for category in categories_data:
        category_name = category['fields']['Название']

        builder.add(InlineKeyboardButton(
            text=category_name,
            callback_data=f"category_{category_name}"
        ))

    builder.adjust(2)
    return builder.as_markup()