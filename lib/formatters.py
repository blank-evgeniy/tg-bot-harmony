from datetime import datetime

def format_seconds_to_time(seconds):
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours}:{minutes:02d}"

def format_slot_date(date_str: str) -> str:
    """Конвертирует '2025-05-04' в '05.04'"""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d.%m")
    except ValueError:
        return date_str