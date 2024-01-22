from aiogram.utils import executor
from handlers import *


executor.start_polling(dp, skip_updates=True)