from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lib.formatters import format_slot_date

def days_kb(dates: list[str]):
    builder = InlineKeyboardBuilder()
    
    for date_str in sorted(dates):
        formatted_date = format_slot_date(date_str)
        builder.button(
            text=formatted_date,
            callback_data=f"date_{date_str}"
        )

    builder.add(InlineKeyboardButton(
        text="Назад",
        callback_data="back_to_procedures"
    ))
    
    builder.adjust(3)
    return builder.as_markup()