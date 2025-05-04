from aiogram import types

async def command_start_handler(message: types.Message) -> None:
    """Обработчик команды /start"""

    welcome_message = (
    '💖 <b>{Name}, добро пожаловать в салон красоты "Harmony"!</b> 💖\n\n'
    "<i>Мы не просто создаем образы — мы раскрываем вашу природную красоту и дарим неповторимые эмоции!</i> 💫"
    )
    
    await message.answer(welcome_message.format(Name=message.from_user.first_name))
