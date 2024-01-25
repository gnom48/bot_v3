from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# кнопка пропустить ввод комментария
def get_skip_rkb() -> ReplyKeyboardMarkup:
    button = KeyboardButton("Пропустить")
    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button)

# кнопка отмены
def get_cancel_rkb() -> ReplyKeyboardMarkup:
    button = KeyboardButton("Отмена записи")
    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button)