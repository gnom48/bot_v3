from aiogram.dispatcher.filters.state import StatesGroup, State

class WorkStates(StatesGroup):

    ready = State()

    enter_fio = State()
    enter_phone = State()
    enter_budget = State()
    enter_object_type = State()
    enter_object_type_commercial = State()
    enter_object_type_private = State()
    enter_object_type_other = State()
    enter_object_location = State()
    enter_comment = State()