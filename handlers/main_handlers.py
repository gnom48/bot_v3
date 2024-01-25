from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from bot import *
from keybords import *
from .utils import *
from .talks import *
from .notifications import take_old_posts, take_new_posts
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio


bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

main_scheduler = AsyncIOScheduler(timezone="UTC")

main_scheduler.add_job(func=take_new_posts, trigger=IntervalTrigger(hours=2), kwargs={"bot": bot, "dp": dp, "source": "source.txt"})


# при старте бота
async def on_start_bot(_):
    await take_old_posts(bot=bot, dp=dp, source="source.txt")


# команда старт
@dp.message_handler(commands=['start'], state="*")
async def start_cmd(msg: types.Message):
    await msg.answer(text=hello_message, reply_markup=get_main_menu_ikb(), parse_mode="HTML")
    await WorkStates.ready.set()


# слушает ввод инлайн клавиатуры главного меню
@dp.callback_query_handler(state=WorkStates.ready)
async def main_menu_clicks(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("✓")
    
    if callback.data == "resources":
        await bot.send_message(chat_id=callback.from_user.id, text="Выберите интересующую вас ссылку:", reply_markup=get_official_links_ikb())
        await asyncio.sleep(3)
        await bot.send_message(chat_id=callback.from_user.id, text=restart_message, reply_markup=get_main_menu_ikb(), parse_mode="HTML")
        await WorkStates.ready.set()
    
    elif callback.data == "map":
        await bot.send_message(chat_id=callback.from_user.id, text=map_text, reply_markup=get_map_link_ikb(), parse_mode="HTML")
        await asyncio.sleep(3)
        await bot.send_message(chat_id=callback.from_user.id, text=restart_message, reply_markup=get_main_menu_ikb(), parse_mode="HTML")
        await WorkStates.ready.set()
    
    elif callback.data == "consult":
        await bot.send_message(chat_id=callback.from_user.id, text="Отлично!\n\nДавайте я помогу вам оставить заявку на бесплатную консультацию.", reply_markup=types.ReplyKeyboardRemove())
        await bot.send_message(chat_id=callback.from_user.id, text="Введите свое имя (как наш сотрудник сможет к вам обращаться):", reply_markup=get_cancel_rkb())
        await WorkStates.enter_fio.set()


# ввод имени
@dp.message_handler(state=WorkStates.enter_fio)
async def enter_fio_handler(msg: types.Message, state: FSMContext):
    if (msg.text == "Отмена записи"):
        await bot.send_message(chat_id=msg.from_user.id, text="Ничего страшного, возможно в следующий раз вы захотите получить консультацию. Будем ждать вас снова.", reply_markup=types.ReplyKeyboardRemove())
        await asyncio.sleep(3)
        await bot.send_message(chat_id=msg.from_user.id, text=restart_message, reply_markup=get_main_menu_ikb(), parse_mode="HTML")
        await WorkStates.ready.set()
        return

    if len(msg.text) < 1:
        await msg.answer(text="Боюсь вы ввели непонятное имя, советую указать, как к вам сможет обращаться наш сотрудник.")
        await msg.answer(text="Теперь попробуйте еще раз:")
        return
        
    async with state.proxy() as data:
        data["fio"] = msg.text

    await msg.answer(text=f"Отлично, <b>{msg.text}</b>, теперь введите контактный номер телефона в формате <b>+7(777)777-77-77</b>, чтобы наш сотрудник смог связаться с вами в ближайшее время:", parse_mode="HTML")
    
    await WorkStates.enter_phone.set()


# ввод номера телефона
@dp.message_handler(state=WorkStates.enter_phone)
async def enter_phone_handler(msg: types.Message, state: FSMContext):
    if (msg.text == "Отмена записи"):
        await bot.send_message(chat_id=msg.from_user.id, text="Ничего страшного, возможно в следующий раз вы захотите получить консультацию. Будем ждать вас снова.", reply_markup=types.ReplyKeyboardRemove())
        await asyncio.sleep(3)
        await bot.send_message(chat_id=msg.from_user.id, text=restart_message, reply_markup=get_main_menu_ikb(), parse_mode="HTML")
        await WorkStates.ready.set()
        return

    if not check_phone_number(msg.text):
        await msg.answer(text="Боюсь вы ввели некорректный номер телефона, советую указать телефон, по которому с вами можно будет связаться.")
        await msg.answer(text="Теперь попробуйте еще раз:")
        return

    await msg.answer(text=f"Отлично, теперь выберите тип недвижимости, которая вас интересует:", reply_markup=get_object_types_ikb())
    
    async with state.proxy() as data:
        data["phone"] = msg.text
    
    await WorkStates.enter_object_type.set()


# слушает ввод инлайн клавиатуры типа недвижимости
@dp.callback_query_handler(state=WorkStates.enter_object_type)
async def object_types_clicks(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("✓")
    
    if callback.data == "private":
        async with state.proxy() as data:
            data["type1"] = "Частаня"

        await bot.send_message(chat_id=callback.from_user.id, text="Хорошо, теперь давайте уточним категорию:", reply_markup=get_private_object_types_ikb())
        await WorkStates.enter_object_type_private.set()
        return

    elif callback.data == "commercial":
        async with state.proxy() as data:
            data["type1"] = "Коммерческая"

        await bot.send_message(chat_id=callback.from_user.id, text="Хорошо, теперь давайте уточним категорию:", reply_markup=get_commercial_object_types_ikb())
        await WorkStates.enter_object_type_commercial.set()
        return

    else:
        print("Что-то пошло не так")
        
        
# слушает ввод инлайн клавиатуры ЧАСТОЙ недвижимости
@dp.callback_query_handler(state=WorkStates.enter_object_type_private)
async def private_object_types_clicks(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("✓")
    
    async with state.proxy() as data:
        if callback.data == "flat":
            data["type2"] = "Квартира"
        elif callback.data == "dacha":
            data["type2"] = "Земельный участок"   
        elif callback.data == "house":
            data["type2"] = "Дом"
        elif callback.data == "garage":
            data["type2"] = "Гараж"
        elif callback.data == "other":
            await bot.send_message(chat_id=callback.from_user.id, text="Понял, вам нужно что-то особенное! \n\nВы можете ввести название недвижимости, которая вас интересует самостоятельно:")
            await WorkStates.enter_object_type_other.set()
            return
        else:
            print("Что-то пошло не так")
            return

    await bot.send_message(chat_id=callback.from_user.id, text="Отлично, теперь чтобы давайте уточним ваш предполагемый бюджет, чтобы нас специалист смог подготовиться:", reply_markup=types.ReplyKeyboardRemove())
    await WorkStates.enter_budget.set()

    
# слушает ввод инлайн клавиатуры КОММЕРЧЕСКОЙ недвижимости
@dp.callback_query_handler(state=WorkStates.enter_object_type_commercial)
async def commercial_object_types_clicks(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("✓")
    
    async with state.proxy() as data:
        if callback.data == "office":
            data["type2"] = "Офис"
        elif callback.data == "stock":
            data["type2"] = "Склад"   
        elif callback.data == "shop":
            data["type2"] = "Магазин"
        elif callback.data == "other":
            await bot.send_message(chat_id=callback.from_user.id, text="Понял, вам нужно что-то особенное! \n\nВы можете ввести название недвижимости, которая вас интересует самостоятельно:")
            await WorkStates.enter_object_type_other.set()
            return
        else:
            print("Что-то пошло не так")
            return
        
    await bot.send_message(chat_id=callback.from_user.id, text="Отлично, теперь чтобы давайте уточним ваш предполагемый бюджет, чтобы нас специалист смог подготовться:", reply_markup=types.ReplyKeyboardRemove())
    await WorkStates.enter_budget.set()


# ввод ОСОБЕННОЙ категории недвижимотси
@dp.message_handler(state=WorkStates.enter_object_type_other)
async def enter_other_object_type_handler(msg: types.Message, state: FSMContext):
    if len(msg.text) < 1:
        await msg.answer(text="Боюсь вы ввели непонятное название, чем точнее вы опишите интересующую вас категорию, тем лучше наш специалист сможет подготовиться к встрече.")
        await msg.answer(text="Теперь попробуйте еще раз:")
        return
        
    async with state.proxy() as data:
        data["type2"] = msg.text
    
    await bot.send_message(chat_id=msg.from_user.id, text="Отлично, теперь чтобы давайте уточним ваш предполагемый бюджет (в рублях), чтобы нас сотрудник смог подготовться:", reply_markup=types.ReplyKeyboardRemove())
    await WorkStates.enter_budget.set()


# ввод предполагаемого бюджета
@dp.message_handler(state=WorkStates.enter_budget)
async def enter_other_object_type_handler(msg: types.Message, state: FSMContext):
    budget = -1
    try:
        budget = int(msg.text)
    except ValueError:
        await msg.answer(text="Боюсь вы ввели некорректное число.")
        await msg.answer(text="Теперь попробуйте еще раз:")
        return
    except Exception:
        await msg.answer(text="Теперь попробуйте еще раз:")
        return
    finally:
        if budget < 0:
            await msg.answer(text="Боюсь вы ввели некорректное число.")
            await msg.answer(text="Теперь попробуйте еще раз:")
            return
        
    async with state.proxy() as data:
        data["budget"] = budget
    
    await bot.send_message(chat_id=msg.from_user.id, text="Отлично, теперь вы можете дописать важные по вашему мнению сведения в комментарий, который увидит наш сотрудник при рассмотрении вашей заявки.", reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(chat_id=msg.from_user.id, text="Если вы не хотите ничего писать просто нажмите кнопку \"Пропустить\"", reply_markup=get_skip_rkb())
    await WorkStates.enter_comment.set()


# ввод комментария
@dp.message_handler(state=WorkStates.enter_comment)
async def enter_comment_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if msg.text == "Пропустить":
            data["comment"] = "Нет"
        else: 
            data["comment"] = msg.text

        await bot.send_message(chat_id=ADMIN_CHAN_ID, text=create_post(data["fio"], data["phone"], data["type1"], data["type2"], data["budget"], data["comment"]), parse_mode="HTML")

    await bot.send_message(chat_id=msg.from_user.id, text="Замечательно, вы успешно заполнили заявку на консультацию!\n\nОчень скоро с вами свяжется один из наших сотрудников и проконсультирует вас в вашем вопросе.", reply_markup=types.ReplyKeyboardRemove())
    
    await msg.answer(text=restart_message, reply_markup=get_main_menu_ikb(), parse_mode="HTML")
    await WorkStates.ready.set()
