import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
import logging
from aiogram import types

#? --------- local moduls ------------
from data.config import ADMINS, COMMANDS_LIST, flag
from keyboards.default.menu_keyboards import admin_panel_btn
from loader import dp, db, bot
from states.reklamaData import ReklamaData
from functions.all_functions import (admin_filter,
                                     get_user_data,
                                     message_fillter)




#? ------------------- userlarga elon / reklama yuborish -----------------------
# @dp.message_handler(text="/reklama", user_id=ADMINS)
# @dp.message_handler(text_contains="/reklama")
@dp.message_handler(text_contains="💭", state=None)
async def go_send_to_all(message: types.Message, state: FSMContext):
    logging.info("reklama")
    language, user_obj, tel_id = await get_user_data(message)
    ADMINS_LIST = await admin_filter(flag, admin_list=ADMINS)

    if str(tel_id) in ADMINS_LIST:
        # Обработка случаев, когда оба значения не None
        msg_ru = "💭 Введите текст объявления 👇"
        msg_uz = "💭 E'lon tekstini kiriting 👇"
        msg = await message_fillter(language, msg_ru, msg_uz)
        await message.answer(msg, reply_markup=ReplyKeyboardRemove())
        await ReklamaData.text_reklama.set()
    else:
        # Обработка остальных случаев
        pass


@dp.message_handler(state=ReklamaData.text_reklama, content_types=["text", types.ContentType.PHOTO])
async def send_to_all(message: types.Message, state: FSMContext):
    logging.info("reklama text -----------")
    language, user, tel_id = await get_user_data(message)

    if message.text not in COMMANDS_LIST:
        msg = message.text
        all_users_obj_list = await db.select_all_users()

        # Admin e'loni barcha userlarga
        if tel_id == 82640514:
            logging.info("reklama text from admin")
            for user_obj in all_users_obj_list:
                logging.info(user_obj)
                if message.content_type == "text":
                    await bot.send_message(chat_id=user_obj[5], text=f"💭\n{msg}")
                elif message.content_type == "photo":
                    photo_id = message.photo[-1].file_id
                    caption = message.caption
                    await bot.send_photo(chat_id=user_obj[5], photo=photo_id, caption=caption)
                await asyncio.sleep(0.05)
            # await message.answer(f"E'lon yuborildi.", reply_markup=await business_panel_btn(language))
            await state.finish()
        else:
            pass
    else:
        logging.info("error reklama")
        msg_ru = "💭 Введите текст объявления 👇"
        msg_uz = "💭 E'lon tekstini kiriting 👇"
        msg = await message_fillter(language, msg_ru, msg_uz)
        await message.answer(msg)