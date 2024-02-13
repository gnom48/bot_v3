from keybords import reply_keybords
from .utils import *
from aiogram.utils.exceptions import RetryAfter
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from bot.consts import BOT_LINK, PUBLIC_CHAN_ID
import html
import asyncio


async def take_old_posts(bot: Bot, dp: Dispatcher) -> None:
    hatas = get_first_n(n=3)
    #print("take_old_posts", hatas, "\n", sep="\n")

    for hata in hatas:
        media_group = []
        if len(hata.pics) == 0:
            hata.pics.append("https://sun9-71.userapi.com/impg/RdQ3eD5VkTMcHJcqqGyDuRBNOItdF-M0doeu3Q/9stPIL-4bXk.jpg?size=1466x2160&quality=95&sign=9d96b643e244a2c21546a4fe0f27f300&type=album")
        # media = types.InputMediaPhoto(media=hata.pics[0], caption=f"📣<b>Новый объект ({hata.advert_type})!</b> #{hata.id} 📣\n\n<i><u>{hata.title}</u></i>\n\nТип недвижимости: {hata.type}\nЭтаж: {hata.floor}\nЦена: {hata.price}\nАдрес: {hata.address}\n\n" + f"""Подробная информация по <u><a href="{'https://proestate.24sn.ru' + hata.link[0]}">{html.escape("ссылке")}</a></u>""", parse_mode=types.ParseMode.HTML)
        media = types.InputMediaPhoto(media=hata.pics[0], caption=f"📣<b> Новый объект ({hata.advert_type})!</b> 📣\n#{hata.id}\n\n<i><u>{hata.title}</u></i>\n\nТип недвижимости: {hata.type}\nЭтаж: {hata.floor}\nЦена: {hata.price}\nПлощадь: {hata.square}\nАдрес: {hata.address}\n\n" + f"""Заинтересовал объект? Оставь заявку на консультацию со специалистом в нашем <u><a href="{BOT_LINK}">{html.escape("боте")}</a></u>""", parse_mode=types.ParseMode.HTML)
        if len(hata.pics) > 1:
            media_group = [types.InputMediaPhoto(media=url) for url in hata.pics[1:]]
        media_group.append(media)
        
        max_retries = 3
        retries = 0
        while retries < max_retries:
            try:
                await bot.send_media_group(chat_id=PUBLIC_CHAN_ID, media=media_group)
                break
            except RetryAfter as e:
                await asyncio.sleep(e.timeout)
                retries += 1
                continue


async def take_new_posts(bot: Bot, dp: Dispatcher) -> None:
    hatas = find_new()
    #print("take_new_posts", hatas, "\n", sep="\n")

    for hata in hatas:
        media_group = []
        if len(hata.pics) == 0:
            hata.pics.append("https://sun9-71.userapi.com/impg/RdQ3eD5VkTMcHJcqqGyDuRBNOItdF-M0doeu3Q/9stPIL-4bXk.jpg?size=1466x2160&quality=95&sign=9d96b643e244a2c21546a4fe0f27f300&type=album")
        # media = types.InputMediaPhoto(media=hata.pics[0], caption=f"📣<b>Новый объект ({hata.advert_type})!</b> #{hata.id} 📣\n\n<i><u>{hata.title}</u></i>\n\nТип недвижимости: {hata.type}\nЭтаж: {hata.floor}\nЦена: {hata.price}\nАдрес: {hata.address}\n\n" + f"""Подробная информация по <u><a href="{'https://proestate.24sn.ru' + hata.link[0]}">{html.escape("ссылке")}</a></u>""", parse_mode=types.ParseMode.HTML)
        media = types.InputMediaPhoto(media=hata.pics[0], caption=f"📣<b> Новый объект ({hata.advert_type})!</b> 📣\n#{hata.id}\n\n<i><u>{hata.title}</u></i>\n\nТип недвижимости: {hata.type}\nЭтаж: {hata.floor}\nЦена: {hata.price}\nПлощадь: {hata.square}\nАдрес: {hata.address}\n\n" + f"""Заинтересовал объект? Оставь заявку на консультацию со специалистом в нашем <u><a href="{BOT_LINK}">{html.escape("боте")}</a></u>""", parse_mode=types.ParseMode.HTML)
        if len(hata.pics) > 1:
            media_group = [types.InputMediaPhoto(media=url) for url in hata.pics[1:]]
        media_group.append(media)

        max_retries = 3
        retries = 0
        while retries < max_retries:
            try:
                await bot.send_media_group(chat_id=PUBLIC_CHAN_ID, media=media_group)
                break
            except RetryAfter as e:
                await asyncio.sleep(e.timeout)
                retries += 1
                continue
