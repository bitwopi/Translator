from aiogram.dispatcher.filters.state import State, StatesGroup


class LangStates(StatesGroup):
    LANG_CHANGED = State()
    LANG_SET = State()
