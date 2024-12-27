import logging
from aiogram import Dispatcher

from functions.all_functions import admin_filter
from data.config import ADMINS, flag




async def on_startup_notify(dp: Dispatcher):
    ADMINS_LIST = await admin_filter(flag, admin_list=ADMINS)
    for admin in ADMINS_LIST:
        try:
            if admin == '82640514':
                await dp.bot.send_message(admin, "Bot ishga tushdi")
        except Exception as err:
            logging.exception(err)