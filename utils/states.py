from aiogram.fsm.state import State, StatesGroup

class Distribution(StatesGroup):
    text = State()
    photo = State()

    