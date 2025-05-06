from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime

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

def format_slot_date(date_str: str) -> str:
    """Конвертирует '2025-05-04' в '05.04'"""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d.%m")
    except ValueError:
        return date_str