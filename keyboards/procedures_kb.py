from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def procedures_kb(procedures_data):
    builder = InlineKeyboardBuilder()

    for procedure in procedures_data:
        id = procedure["id"]
        name = procedure['fields']['Название']
        price = procedure['fields']['Стоимость']

        builder.add(InlineKeyboardButton(
            text=f"{name} - {price}₽",
            callback_data=f"procedure_{id}"
        ))

    builder.add(InlineKeyboardButton(
        text="Назад к категориям",
        callback_data="back_to_categories"
    ))

    builder.adjust(1)
    return builder.as_markup()