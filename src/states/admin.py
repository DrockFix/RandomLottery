from aiogram.fsm.state import StatesGroup, State


class AdminMenu(StatesGroup):
    main = State()
    license = State()
    stat = State()
    dict = State()

