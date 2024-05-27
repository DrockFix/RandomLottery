from aiogram.fsm.state import StatesGroup, State


class MenuUser(StatesGroup):
    main = State()
    events = State()
    help = State()
    contact = State()
    stat = State()
    settings = State()


class AddEvent(StatesGroup):
    type_event = State()
    title = State()
    url = State()
    date = State()
    confirm = State()
    result = State()


class DeleteEvent(StatesGroup):
    confirm = State()
    result = State()


class EditEvent(StatesGroup):
    type_event = State()
    title = State()
    url = State()
    date = State()
    confirm = State()
    result = State()
