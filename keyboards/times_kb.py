from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lib.formatters import format_seconds_to_time

def times_kb(dates):
    builder = InlineKeyboardBuilder()
    
    time_ranges = {}
    
    for date in dates:
        start_time = date['fields']['Время начала']
        end_time = date['fields']['Время окончания']
        slot_id = date['fields']['id']
        
        time_key = (start_time, end_time)

        if time_key not in time_ranges:
            time_ranges[time_key] = []

        time_ranges[time_key].append(slot_id)
    
    sorted_ranges = sorted(time_ranges.keys())
    
    for start_time, end_time in sorted_ranges:
        formatted_range = f"{format_seconds_to_time(start_time)} - {format_seconds_to_time(end_time)}"
        
        slot_ids = time_ranges[(start_time, end_time)]
        slot_id = slot_ids[0]
        
        builder.button(
            text=formatted_range,
            callback_data=f"time_{start_time}_{end_time}_{slot_id}"
        )
    
    builder.add(InlineKeyboardButton(
        text="Назад",
        callback_data="back_to_dates"
    ))
    
    builder.adjust(3)
    return builder.as_markup()