from aiogram.fsm.state import State, StatesGroup

class Distribution(StatesGroup):
    text = State()
    photo = State()

class Ticket(StatesGroup):
    text = State()
    priority = State()

class AnswerTicket(StatesGroup):
    id = State()
    text = State()

    