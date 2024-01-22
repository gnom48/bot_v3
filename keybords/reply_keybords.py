from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# кнопка пропустить ввод комментария
def get_skip_rkb() -> ReplyKeyboardMarkup:
    button = KeyboardButton("Пропустить")
    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button)