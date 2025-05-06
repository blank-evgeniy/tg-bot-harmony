from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lib.formatters import format_seconds_to_time

def times_kb(dates):
    builder = InlineKeyboardBuilder()
    unique_ranges = set() 

    for date in dates:
        start_time = date['fields']['Время начала']
        end_time = date['fields']['Время окончания']
        unique_ranges.add((start_time, end_time)) 

    sorted_ranges = sorted(unique_ranges)

    for start_time, end_time in sorted_ranges:
        formatted_range = f"{format_seconds_to_time(start_time)} - {format_seconds_to_time(end_time)}" 
        builder.button(
            text=formatted_range,
            callback_data=f"time_{start_time}_{end_time}" 
        )

    builder.add(InlineKeyboardButton(
        text="Назад",
        callback_data="back_to_dates"
    ))
    
    builder.adjust(3)
    return builder.as_markup()
