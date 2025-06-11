from aiogram.fsm.state import StatesGroup, State

class BookingStates(StatesGroup):
    waiting_for_master = State()
    waiting_for_procedure = State()
    waiting_for_date = State()
    waiting_for_time = State()