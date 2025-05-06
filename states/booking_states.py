from aiogram.fsm.state import StatesGroup, State

class BookingStates(StatesGroup):
    waiting_for_procedure = State()