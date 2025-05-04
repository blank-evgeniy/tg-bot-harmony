from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def request_contact_kb():
    keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text="📱 Отправить телефон", 
                    callback_data="share_phone"
                )]
            ]
        )
    return keyboard