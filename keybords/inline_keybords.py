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
            InlineKeyboardMarkup(text="Официальный сайт", url=WEBSITE_LINL))
    return ikb


# ссылка на карту
def get_map_link_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardMarkup(text="Яндекс карты", url=Y_MAPS_LINK))
    return ikb


# типы недвижимости
def get_object_types_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardButton(text="👨‍👩‍👦 Частная", callback_data="private"),
            InlineKeyboardButton(text="👔 Коммерческая", callback_data="commercial"))
    return ikb


# виды частной недвижимости
def get_private_object_types_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardButton(text="🏢 Квартира", callback_data="flat"),
            InlineKeyboardButton(text="🌳 Земля", callback_data="dacha"),
            InlineKeyboardButton(text="🏡 Земля с домом", callback_data="house"),
            InlineKeyboardButton(text="📝 Другое", callback_data="other"))
    return ikb


# виды коммерческой недвижимости
def get_commercial_object_types_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardButton(text="🖨 Офис", callback_data="office"),
            InlineKeyboardButton(text="📦 Склад", callback_data="stock"),
            InlineKeyboardButton(text="🛒 Магазин", callback_data="shop"),
            InlineKeyboardButton(text="📝 Другое", callback_data="other"))
    return ikb