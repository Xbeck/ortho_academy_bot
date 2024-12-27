import logging
import re
from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

# -------------- local moduls ----------------

from keyboards.inline.user_account_keyboards import show_servis_type_btn
from loader import dp, bot, db
from data.config import ADMINS, COMMANDS_LIST, flag
# from keyboards.inline.doc_to_user_keyboard import admin_to_user_btn
from states.sendMessage import FromUserToDoc
from keyboards.default.menu_keyboards import (
                                              user_panel_btn)
from functions.all_functions import (
                                    admin_filter,
                                    get_user_data,
                                    message_fillter,
                                    question_title)



# user accountga o'tish
# @dp.message_handler(commands='user_account')
# async def create_business_account(message: types.Message):
#     logging.info('show user account interface')
#     language, user_obj, tel_id = await get_user_data(message)

#     try:
#         businiss_account = await db.exists_business_account(user_obj['id'])
#     except Exception as e:
#         logging.info(e)

#     if businiss_account:
#         logging.info("questions + business btn")
#         msg1, msg2 = await question_title(language)
#         await message.answer(msg1 + msg2, reply_markup=await question_btn(user_obj=user_obj, language=language))

#         # await message.answer("Docs", reply_markup=await show_business_account_btn(referral_id, language))

#         msg_ru = "⚠️\nВнешний вид интерфейса для ваших клиентов!"
#         msg_uz = "⚠️\nKlientlariz uchun interface ni ko'rinishi!"
#         msg = await message_fillter(language, msg_ru, msg_uz)
#         await message.answer(msg, reply_markup=await user_panel_btn(language))
#     else:
#         logging.info("not businis account")













# #? ---------------------------- send to Doc message ----------------------------
# @dp.message_handler(text_contains="📨", state=None)
# async def get_message_from_user(message: types.Message):
#     msg_ru = "Введите свой вопрос!"
#     msg_uz = "Savolingizni kiriting!"
#     language, user, tel_id = await get_user_data(message)
#     msg = await message_fillter(language, msg_ru, msg_uz)

#     await message.answer(msg, reply_markup=ReplyKeyboardRemove())
#     await FromUserToDoc.message_text.set()


# @dp.message_handler(state=FromUserToDoc.message_text)
# async def send_to_doc(message: types.Message, state: FSMContext):
#     language, user, tel_id = await get_user_data(message)
#     question = message.text

#     if question not in COMMANDS_LIST:
#         # question = f"From: @{message.from_user.username}\n{question}"
#         question = f"From: {user['full_name']}\n{question}"
#         # ADMINS_LIST = await admin_filter(flag, admin_list=ADMINS)
#         await bot.send_message(chat_id=user["referral_id"], text=question,
#                                reply_markup=admin_to_user_btn(language=language, call_back=str(tel_id)))

#         msg = await message_fillter(language,
#                               "✅ Вопрос отправлен!",
#                               "✅ Savol yuborildi!")
        
#         business_account = await db.exists_business_account(user['id'])
#         if business_account:
#             await message.answer(msg, reply_markup=await business_panel_btn(language))
#             await state.finish()
#         else:
#             msg1, msg2 = await question_title(language)
#             await message.answer(msg1, reply_markup=await user_panel_btn(language))
#             await message.answer(msg2, reply_markup=await question_btn(user_obj=user, language=language))
#             await state.finish()
#     else:
#         msg_ru = "Введите свой вопрос!"
#         msg_uz = "Savolingizni kiriting!"
#         msg = await message_fillter(language, msg_ru, msg_uz)
#         await message.answer(msg)


# # doc qabuliga yozilish, xizmat turini tanlash
# @dp.message_handler(text_contains='📝')
# async def create_business_account(message: types.Message):
#     logging.info('see servis types')
#     language, user_obj, tel_id = await get_user_data(message)

#     msg_ru = "Выберите тип услуги"
#     msg_uz = "Xizmat turini tanlang"
#     msg = await message_fillter(language, msg_ru, msg_uz)

#     try:
#         user_business_obj = await db.select_user(int(user_obj['referral_id']))
#         business_obj = await db.select_businesses(user_business_obj['id'])
#     except Exception as e:
#         logging.info(e)
#         business_obj = None

#     if business_obj != None:
#         service_list = business_obj['servis_type']
#         # await message.answer(msg, reply_markup=await user_panel_btn(user_obj["language"]))
#         await message.answer(msg, reply_markup=await show_servis_type_btn(service_list, language))
#     else:
#         logging.info("")
#         msg_ru = "Информация еще не добавлена"
#         msg_uz = "Hali ma'lumot qo'shilmagan"
#         msg = await message_fillter(language, msg_ru, msg_uz)
#         await message.answer(msg)



