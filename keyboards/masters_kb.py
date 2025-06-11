from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def masters_kb(masters_data):
    builder = InlineKeyboardBuilder()
    
    for master in masters_data:
        master_name = master['fields']['Имя']
        master_id = master['id']

        builder.add(InlineKeyboardButton(
            text=master_name,
            callback_data=f"master_{master_id}"
        ))

    builder.add(InlineKeyboardButton(
        text="Назад",
        callback_data="back_to_categories"
    ))

    builder.adjust(1)
    return builder.as_markup()