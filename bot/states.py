from aiogram.fsm.state import State, StatesGroup

class CreateEvent(StatesGroup):
    title = State()
    time = State()
    chat_id = State()
    thread_id = State()