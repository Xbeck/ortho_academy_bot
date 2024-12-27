# from aiogram import types
# from aiogram.dispatcher.filters.builtin import CommandStart
# import logging
# import asyncpg

# from functions.all_functions import admin_filter, get_user_data, message_fillter, question_title
# from data.config import ADMINS, flag
# from keyboards.default.menu_keyboards import admin_panel_btn, business_panel_btn, user_panel_btn
# from keyboards.inline.question_keyboards import question_btn
# from keyboards.inline.registration_keyboard import register_btn
# from keyboards.inline.language_keyboards import language_btn
# from loader import dp, db, bot


import logging
from unittest import result

from aiogram import types
from data.config import ADMINS, CHANNELS, flag
from functions.all_functions import admin_filter, message_fillter
from handlers.users.market_handlers import generate_product_info
from keyboards.default.menu_keyboards import admin_panel_btn, user_panel_btn
from keyboards.inline.registration_keyboard import register_btn
from keyboards.inline.subscription_keyboards import check_button
from loader import dp, db, bot
from utils.misc import subscription



@dp.message_handler(commands=['start'])
async def show_channels(message: types.Message):
    tel_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    language = "uz"
    try:
        user = await db.user_exists(int(tel_id))
    except Exception as e:
        logging.info(e)
        user = None

    logging.info(user)
    logging.info(tel_id)

    channel = CHANNELS
    logging.info(channel)
    status = await subscription.check(user_id=message.from_user.id, channel=channel)
    logging.info(status)


    if status == False:
        logging.info("status False")
        channels_format = str()
        for channel in CHANNELS:
            chat = await bot.get_chat(channel)
            invite_link = await chat.export_invite_link()
            # logging.info(invite_link)
            channels_format += f"👉 <a href='{invite_link}'>{chat.title}</a>\n"
        msg_uz = f"Botdan foydalanish uchun, quyidagi kanallarga obuna bo'ling: \n"
        msg_ru = f"Чтобы использовать бота, подпишитесь на следующие каналы: \n"
        msg = await message_fillter(language, msg_ru, msg_uz)
        await message.answer(msg + channels_format,
                             reply_markup=await check_button(language),
                             disable_web_page_preview=True)
    else:
        logging.info("status True")
        if str(tel_id) in ADMINS:
            logging.info("admin panel")
            msg_uz = f"Salom Master"
            msg_ru = f"Привет Мастер"
            msg = await message_fillter(language, msg_ru, msg_uz)
            await message.answer(msg, reply_markup=await admin_panel_btn(language))
        else:
            logging.info("user panel")
            msg_uz = f"Tavarlar"
            msg_ru = f"Товары"
            msg = await message_fillter(language, msg_ru, msg_uz)
            await message.answer(msg, reply_markup=await user_panel_btn(language=language))
            # await generate_product_info(language=language, message=message, product_num=1)

    if user:
        logging.info("for exsist users")
        await message.answer(f"Menu")
    else:
        msg_ru = "Вы еще не зарегистрированы!"
        msg_uz = "Siz hali Ro'yxatdan o'tmagansiz!"
        msg = await message_fillter(language, msg_ru, msg_uz)
        await message.answer(msg, reply_markup=types.ReplyKeyboardRemove())

        msg_ru = "Пожалуйста, Зарегистрируйтесь 👇"
        msg_uz = "Iltimos Ro'yxatdan o'ting 👇"
        msg = await message_fillter(language, msg_ru, msg_uz)
        await message.answer(msg, reply_markup=await register_btn(language))


@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    language = "uz"
    result = str()
    for channel in CHANNELS:
        status = await subscription.check(user_id=call.from_user.id, channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            msg_uz = f"kanaliga obuna bo'ldingiz!"
            msg_ru = f"вы подписались на канал!"
            msg = await message_fillter(language, msg_ru, msg_uz)
            result += f"✅ <b>{channel.title}</b> {msg}\n\n"
        else:
            invite_link = await channel.export_invite_link()
            msg_uz = f"kanaliga obuna bo'lmagansiz."
            msg_ru = f"вы не подписаны на канал."
            msg_1 = await message_fillter(language, msg_ru, msg_uz)
            msg_uz = f"Obuna bo'ling"
            msg_ru = f"Подписывайся"
            msg_2 = await message_fillter(language, msg_ru, msg_uz)

            result += (f"❌ <b>{channel.title}</b> {msg_1}"
            f"<a href='{invite_link}'>{msg_2}</a>\n\n")

    await call.message.answer(result, disable_web_page_preview=True)
    await call.answer()


@dp.callback_query_handler(text_contains="language")
async def users_registration(call: types.CallbackQuery):
    language = str(call.data).split(",")[-1]
    tel_id = call.from_user.id

    await db.update_user_language(language, tel_id)
    username = call.from_user.username
    phone = await db.get_phone_number(telegram_id=tel_id)
    ADMINS_LIST = await admin_filter(flag, admin_list=ADMINS)

    logging.info("User already registered")

    try:
        user = await db.select_user(telegram_id=tel_id)
    except Exception as e:
        logging.error(f"Error fetching user: {e}")

    if user["language"] is not None:
        await db.update_user_language(language, tel_id)
        logging.info("Language updated")
        msg = await message_fillter(language, "Язык изменился.", "Til o'zgardi.")
        
        if str(tel_id) in ADMINS_LIST:
            logging.info("Admin panel")
            await call.message.answer(msg, reply_markup=await admin_panel_btn(language))
        else:
            logging.info("User panel")
            msg = await message_fillter(language, "Язык изменился.", "Til o'zgardi.")
            await call.message.answer(f"{msg}", reply_markup=await user_panel_btn(user["language"]))
        await call.answer()
