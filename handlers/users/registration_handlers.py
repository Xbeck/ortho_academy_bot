import logging
import re
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
import asyncpg

# ---------------- local moduls ----------------
from loader import dp, bot, db
from data.config import ADMINS, COMMANDS_LIST, flag
from states.personalData import PersonalData

from keyboards.default.start_keyboards import phone_btn
from keyboards.default.menu_keyboards import admin_panel_btn, user_panel_btn
from functions.all_functions import (
                                    admin_filter,
                                    get_user_data,
                                    message_fillter,
                                    question_title)




@dp.callback_query_handler(text_contains="register")
async def bot_registration(call: CallbackQuery):
    # language, user_obj, tel_id = await get_user_data(call)
    language = "uz"
    # await call.message.edit_reply_markup()

    msg_ru = "Введите свое имя и фамилию"
    msg_uz = "Ismingiz va familiyangizni kiriting"
    # msg_ru = "Нажмите кнопку «Отправить номер телефона» 👇"
    # msg_uz = "Telefon raqamni yuborish tugmasini bosing 👇"
    msg = await message_fillter(language, msg_ru, msg_uz)
    await call.message.answer(msg, reply_markup=ReplyKeyboardRemove())
    # await call.message.answer(msg, reply_markup=await phone_btn(language))
    # await PersonalData.phone.set()
    await PersonalData.full_name.set()
    await call.answer()


#  ------------------------ user familyasini olish ------------------------
@dp.message_handler(state=PersonalData.full_name)
async def answer_name(message: types.Message, state: FSMContext):
    # language, user, tel_id = await get_user_data(message)
    language = "uz"
    msg_ru = "Нажмите кнопку «Отправить номер телефона» 👇"
    msg_uz = "Telefon raqamni yuborish tugmasini bosing 👇"
    if re.findall(r"[a-zA-Zа-яА-Я]", message.text) and message.text not in COMMANDS_LIST:
        full_name = message.text
        await state.update_data({"full_name": full_name})
        msg = await message_fillter(language, msg_ru, msg_uz)
        await message.answer(msg, reply_markup=await phone_btn(language))
        await PersonalData.phone.set()
    else:
        msg_ru = "Пожалуйста, введите ваше имя и фамилию"
        msg_uz = "Iltimos, ismingiz va familiyangizni kiriting"
        msg = await message_fillter(language, msg_ru, msg_uz)
        await message.answer(msg)


# # ------------------------ user name ini olish ------------------------
# # @dp.message_handler(state=PersonalData.name)
# # async def answer_lastname(message: types.Message, state: FSMContext):
# #     language, user, tel_id = await get_user_data(message)
# #     msg_ru = "Введите дату своего рождения: \n\nПример: \tдень/месяц/год\n                    21 12 2021"
# #     msg_uz = "Tug'ilgan sa'nangizni kiriting: \n\nNamuna: \tkun/oy/yil\n                    21 12 2021"

# #     if re.findall(r"[a-zA-Zа-яА-Я]", message.text) and message.text not in COMMANDS_LIST:
# #         name = message.text
# #         await state.update_data({"name": name})
# #         msg = await message_fillter(language, msg_ru, msg_uz)
# #         await message.answer(msg)
# #         await PersonalData.birthday.set()
# #     else:
# #         msg_ru = "Введите ваше фамилию"
# #         msg_uz = "Familyangizni kiriting"
# #         msg = await message_fillter(language, msg_ru, msg_uz)
# #         await message.answer(msg)


# # ------------------------ user tug'ilgan sa'nasini olish ------------------------
# # @dp.message_handler(state=PersonalData.birthday)
# # async def answer_of_birthday(message: types.Message, state: FSMContext):
# #     language, user, tel_id = await get_user_data(message)
# #     msg_ru = "Нажмите кнопку «Отправить номер телефона» 👇"
# #     msg_uz = "Telefon raqamni yuborish tugmasini bosing 👇"
# #     msg = await message_fillter(language, msg_ru, msg_uz)
    
# #     # regulyarniy vrajeniya yordamida tug'ilgan sa'nani tekshiramiz:
# #     if (re.fullmatch(r"\d{8}", message.text) or
# #         re.fullmatch(r"\d{2}\s\d{2}\s\d{4}", message.text) or
# #         re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", message.text) or
# #         re.fullmatch(r"\d{2}-\d{2}-\d{4}", message.text) or
# #         re.fullmatch(r"\d{2}/\d{2}/\d{4}", message.text) and
# #         message.text not in COMMANDS_LIST):
# #         birthday = message.text
# #         data = str(birthday).split()
# #         await state.update_data({"birthday": birthday})
# #         msg = await message_fillter(language, msg_ru, msg_uz)
# #         await message.answer(msg, reply_markup=await phone_btn(language))
# #         await PersonalData.phone.set()
# #     else:
# #         msg_ru = "Введите дату своего рождения: \nПример: день/месяц/год\n                    19 12 2022"
# #         msg_uz = "Tug'ilgan sanangizni kiriting: \nNamuna: kun/oy/yil\n                    19 12 2022"
# #         msg = await message_fillter(language, msg_ru, msg_uz)
# #         await message.answer(msg)


@dp.message_handler(state=PersonalData.phone, content_types=types.ContentType.CONTACT)
async def answer_phone_number(message: types.Message, state: FSMContext):
    # language, user_obj, tel_id = await get_user_data(message)
    language = "uz"

    username = message.from_user.username
    telegram_id = message.from_user.id
    language = "uz"

    # if phoneNumber:
    if message.contact:
        phoneNumber = message.contact.phone_number
        await state.update_data({"phone": phoneNumber})

        # Malumotlar bazasiga yozish:
        data = await state.get_data()
        full_name = data.get("full_name")
        # name = data.get("name")
        # birthday = str(data.get("birthday"))
        # phone = data.get("phone")

        try:
            # await db.update_user_data(full_name=full_name, full_name_tel=full_name_tel, birthday=birthday, phone_number=phone, telegram_id=tel_id)
            await db.add_user(full_name=full_name, username=username, language=language, phone_number=phoneNumber, telegram_id=telegram_id)
        except asyncpg.exceptions.UniqueViolationError:
            pass

        # ADMINGA | Userga xabar berish
        count = await db.count_users()
        ADMINS_LIST = await admin_filter(flag, admin_list=ADMINS)

        for val in ADMINS_LIST:
            if message.from_user.username is not None:
                msg = f"@{username} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
            else:
                msg = f"{full_name} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
            try:
                await bot.send_message(chat_id=int(val), text=msg)
            except Exception as e:
                logging.error(f"Chat ID xato: {e}")

        msg = await message_fillter(language,
                                    "Вы успешно зарегистрировались!\n\n",
                                    "Ro'yxatdan muvaffaqiyatli o'tdingiz!\n\n")
        await message.answer(msg)
        await state.finish()

        msg = await message_fillter(language,
                                    "Добро пожаловать в наш бот!\nВыберите в меню нужный раздел",
                                    "Botimizga Xush kelibsiz!\nMenudan o'zingizga kerakli bo'limni tanlang")

        # admin | user panel
        ADMINS_LIST = await admin_filter(flag, admin_list=ADMINS)

        if str(telegram_id) in ADMINS_LIST:
            logging.info("admin panel")
            await message.answer(msg, reply_markup=await admin_panel_btn(language))
        else:
            logging.info("user panel")
            await message.answer(msg, reply_markup=await user_panel_btn(language))
    else:
        msg = await message_fillter(language,
                                    "Пожалуйста!\nНажмите кнопку «Отправить номер телефона» 👇",
                                    "Iltimos!\nTelefon raqamni yuborish tugmasini bosing 👇")
        await message.answer(msg)
