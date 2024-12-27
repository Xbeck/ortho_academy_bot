from distutils.util import change_root
import imp
import logging
from typing import final
from unittest import result
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from data.config import CHANNELS
from utils.misc import subscription
from loader import bot


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        logging.info("middleware:  1")
        if update.message:
            user = update.message.from_user.id
            logging.info(f"middleware: user_id = {user}")
            # start, help komandalari ga bot javob qaytaradigan qildik:
            if update.message.text in ['/start', '/help']:
                return
        elif update.callback_query:
            user = update.callback_query.from_user.id
            # check_subs tugmasi ga bot javob qaytaradigan qildik:
            if update.callback_query.data == "check_subs":
                return
        else:
            return
        logging.info(user)
        result = "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:\n"
        final_status = True
        # for channel in CHANNELS:
            # logging.info(channel)
        channel = CHANNELS
        status = await subscription.check(user_id=user, channel=channel)

        final_status *= status
        channel = await bot.get_chat(channel)
        if not status:
            invite_link = await channel.export_invite_link()
            result += (f"👉\t\t\t<a href='{invite_link}'>{channel.title}</a>\n")

        if not final_status:
            await update.message.answer(result, disable_web_page_preview=True)
            raise CancelHandler()
