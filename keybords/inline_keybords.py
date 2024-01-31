from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.consts import *


# главное меню
def get_main_menu_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardButton(text="ℹ️ Официальные ресурсы", callback_data="resources"),
            InlineKeyboardButton(text="🗺 Мы на карте", callback_data="map"),
            InlineKeyboardButton(text="👩‍💼 Записаться на консультацию", callback_data="consult"))
    return ikb


# ссылки на ресурсы
def get_official_links_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardMarkup(text="Канал с объявлениями", url=OBJECTS_CHAN_LINK),
            InlineKeyboardMarkup(text="Официальный сайт", url=WEBSITE_LINL),
            InlineKeyboardMarkup(text="Мы ВКонтакте", url=VK_LINL))
    return ikb


# ссылка на карту
def get_map_link_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardMarkup(text="Яндекс карты", url=Y_MAPS_LINK))
    return ikb


# ссылка на бота
def get_bot_link_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardMarkup(text="Заявка на консультацию", url=BOT_LINK))
    return ikb


# типы недвижимости
def get_object_types_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardButton(text="👨‍👩‍👦 Частная", callback_data="private"),
            InlineKeyboardButton(text="👔 Коммерческая", callback_data="commercial"))
    return ikb


# районы
def get_locate_object_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardButton(text="Ленинский", callback_data="Ленинский"),
            InlineKeyboardButton(text="Гагаринский", callback_data="Гагаринский"),
            InlineKeyboardButton(text="Нахимоский", callback_data="Нахимоский"),
            InlineKeyboardButton(text="Балаклавский", callback_data="Балаклавский"),
            InlineKeyboardButton(text="Пригород", callback_data="Пригород"),
            InlineKeyboardButton(text="Не важен", callback_data="Не важен"))
    return ikb


# обобщенные виды недвижимости
def get_all_object_types_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardButton(text="🏢 Дом", callback_data="house"),
            InlineKeyboardButton(text="🌳 Участок", callback_data="dacha"),
            InlineKeyboardButton(text="🏡 Квартира", callback_data="flat"),
            InlineKeyboardButton(text="🛋 Аппартаменты", callback_data="appart"),
            InlineKeyboardButton(text="🧰 Коммерческая недвижимость", callback_data="commercial"),
            InlineKeyboardButton(text="📝 Другое", callback_data="other"))
    return ikb
