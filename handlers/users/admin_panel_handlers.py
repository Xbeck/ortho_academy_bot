import asyncio
import logging
import time
from typing import Union
from aiogram import types
from aiogram.types import CallbackQuery, Message
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

# -------------- local moduls ----------------
from keyboards.inline.doc_admin_keyboards import cource_data_info_btn, cource_info_menu
from loader import dp, bot, db
from data.config import ADMINS, COMMANDS_LIST, flag
from keyboards.inline.language_keyboards import language_btn
from states.personalData import (GetCourseTitle,
                                 GetCourseDiscription,
                                 GetCourseImgUrl,
                                 GetCoursePlan,
                                 GetCoursePrice,
                                 GetCourseDiscount)
from states.sendMessage import FromDocToUser
from keyboards.default.menu_keyboards import admin_panel_btn
from functions.all_functions import (
                                    admin_filter,
                                    get_user_data,
                                    message_fillter)




#? --------------------------- Doc send answer to User -------------------------------
@dp.callback_query_handler(text_contains="admin_to_user", state=None)
async def get_answer_from_doc(call: CallbackQuery, state: FSMContext):
    logging.info("dop_question_answer btn")
    language, user, tel_id = await get_user_data(call)
    user_tel_id = str(call.data).split(",")[-1]

    await state.update_data(
                            {"user_tel_id": user_tel_id})
    msg = await message_fillter(language,
                          "Ответьте на вопрос. 👇",
                          "Savolga javob bering 👇")

    await call.message.edit_reply_markup()
    await call.message.answer(msg, reply_markup=ReplyKeyboardRemove())
    await FromDocToUser.message_text.set()


#? --------------------------------- User savoliga javob tekstini admindan olib User ga yuboramiz: -----------------------
@dp.message_handler(state=FromDocToUser.message_text)
async def send_to_user(message: types.Message, state: FSMContext):
    logging.info("user savoliga javob -----------")
    language, user, tel_id = await get_user_data(message)
    msg = message.text
    data = await state.get_data()
    user_tel_id = data.get("user_tel_id")

    if msg not in COMMANDS_LIST:
        await bot.send_message(chat_id=int(user_tel_id), text=f"Doc javobi:\n{msg}")

        msg = await message_fillter(language,
                              "✅ Ответ отправлен!",
                              "✅ Javob yuborildi!")
        await message.answer(msg, reply_markup=await admin_panel_btn(language))
        await state.finish()
    else:
        msg = await message_fillter(language,
                              "Ответ на вопрос 👇",
                              "Savolga javob bering 👇")
        await message.answer(msg)


# ? ---------------------------- Users count ----------------------------
@dp.message_handler(text_contains="👤")
async def show_users_count(message: types.Message):
    logging.info('user count')
    language, user_obj, tel_id = await get_user_data(message)
    ADMINS_LIST = await admin_filter(flag, admin_list=ADMINS)

    if str(tel_id) in ADMINS_LIST:
        users = await db.count_users()
        logging.info(users)
        msg_ru = f"В базе данных есть пользователи: {users}."
        msg_uz = f"Bazada {users}-ta user bor."
        msg = await message_fillter(language, msg_ru, msg_uz)
        await message.answer(msg)



# ? ---------------------------- Language ----------------------------
@dp.message_handler(text_contains="🇺🇿")
async def show_menu_uz(message: types.Message):
    await menu_categories(message)

@dp.message_handler(text_contains="🇷🇺")
async def show_menu_ru(message: types.Message):
    await menu_categories(message)

async def menu_categories(message: Union[CallbackQuery, Message], **kwargs):
    markup = language_btn
    language, user, tel_id = await get_user_data(message)
    
    # Agar foydalanuvchidan Message kelsa Keyboardni yuboramiz
    if isinstance(message, Message):
        msg_ru = "Выберите язык 👇"
        msg_uz = "Tilni tanlang 👇"
        msg = await message_fillter(language, msg_ru, msg_uz)
        await message.answer(msg, reply_markup=markup)

    # Agar foydalanuvchidan Callback kelsa Callback natbibi o'zgartiramiz
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)



#? --------------------------- doc course -----------------------------
@dp.message_handler(text_contains="📖")
async def show_course_menu(message: types.Message):
    logging.info('show courses')
    await message.answer(text="Barcha kurslar", reply_markup=ReplyKeyboardRemove())
    await message.delete()
    await message.answer("va kurs qo'shish", reply_markup=await cource_info_menu())




#? ------------------------ Back ---------------------------
@dp.callback_query_handler(text_contains="_back_0")
async def bot_back_0(call: types.CallbackQuery):
    logging.info("bot back 0")
    language, user_obj, tel_id = await get_user_data(call)

    if str(tel_id) in ADMINS:
        msg_ru = f"Назад"
        msg_uz = f"Menu"
        msg = await message_fillter(language, msg_ru, msg_uz)
        await call.message.delete()
        await call.message.answer(msg, reply_markup=await admin_panel_btn(language))
        await call.answer()
    else:
        pass


@dp.callback_query_handler(text_contains="_back_1")
async def bot_back_1(call: types.CallbackQuery):
    logging.info("bot back 1")
    language, user_obj, tel_id = await get_user_data(call)

    if str(tel_id) in ADMINS:
        msg_ru = f"Назад"
        msg_uz = f"Barcha kurslar va kurs qo'shish"
        msg = await message_fillter(language, msg_ru, msg_uz)
        await call.message.edit_text(msg)
        await call.message.edit_reply_markup(reply_markup=await cource_info_menu())
        await call.answer()
    else:
        pass


@dp.callback_query_handler(text_contains="_edit_course:")
async def edit_course_info(call: CallbackQuery):
    logging.info('edit course info')
    language, user, tel_id = await get_user_data(call)
    trigger, course_num = call.data.split(":")
    # await call.message.delete()
    await call.message.edit_text("Kurs haqidagi ma'lumotlarni kiriting")
    await call.message.edit_reply_markup(reply_markup=await cource_data_info_btn(course_num=int(course_num)))


@dp.callback_query_handler(text_contains="_add_course:")
async def add_new_course(call: CallbackQuery):
    logging.info('add new course')
    language, user, tel_id = await get_user_data(call)

    course_obj = await db.select_courses()
    curse_id_list = []
    for i in course_obj:
        curse_id_list.append(i['id'])
    course_num = sorted(curse_id_list)[-1] + 1

    # await call.message.delete()
    await call.message.edit_text("Kurs haqidagi ma'lumotlarni kiriting")
    await call.message.edit_reply_markup( reply_markup=await cource_data_info_btn(course_num=int(course_num)))







@dp.callback_query_handler(text_contains="_title:")
async def get_course_title(call: CallbackQuery, state: FSMContext):
    logging.info("get course title")
    await state.update_data({"call": call.data})
    await call.message.answer("Kurs sarlavhasini kiriting", reply_markup=ReplyKeyboardRemove())
    await GetCourseTitle.title.set()
    await call.answer()

@dp.callback_query_handler(text_contains="_discription:", state=None)
async def post_course_about(call: CallbackQuery, state: FSMContext):
    logging.info("post course discription")
    await state.update_data({"call": call.data})
    await call.message.answer("Kurs haqidagi ma'lumotni kiriting", reply_markup=ReplyKeyboardRemove())
    await GetCourseDiscription.discription.set()
    await call.answer()

@dp.callback_query_handler(text_contains="_img_url:", state=None)
async def post_course_image(call: CallbackQuery, state: FSMContext):
    logging.info("post course image")
    await state.update_data({"call": call.data})
    await call.message.answer("Kurs rasmini kiriting", reply_markup=ReplyKeyboardRemove())
    await GetCourseImgUrl.img_url.set()
    await call.answer()

@dp.callback_query_handler(text_contains="_plane:", state=None)
async def post_course_plane(call: CallbackQuery, state: FSMContext):
    logging.info("post course plane")
    await state.update_data({"call": call.data})
    await call.message.answer("Kurs rejasini kiriting", reply_markup=ReplyKeyboardRemove())
    await GetCoursePlan.plan.set()
    await call.answer()

@dp.callback_query_handler(text_contains="_price:", state=None)
async def post_course_price(call: CallbackQuery, state: FSMContext):
    logging.info("post course price")
    await state.update_data({"call": call.data})
    await call.message.answer("Kurs narxini so'm da kiriting", reply_markup=ReplyKeyboardRemove())
    await GetCoursePrice.price.set()
    await call.answer()

@dp.callback_query_handler(text_contains="_discount:", state=None)
async def post_course_discount(call: CallbackQuery, state: FSMContext):
    logging.info("post course discount")
    await state.update_data({"call": call.data})
    await call.message.answer("Kursga chegirma bo'lsa kiriting, aks holda 0 ni kiriting", reply_markup=ReplyKeyboardRemove())
    await GetCourseDiscount.discount.set()
    # await save_course_data(message: types.Message, state: FSMContext)
    await call.answer()




async def post_data_to_db(message, triger, course_num, state):
    """
    trigerga qarab filter qiladiva db cours jadvaliga yozadi, state ni tugatadi yo message yo'llaydi
    """
    new_data = ""
    if message.photo and triger=="_img_url":
        new_data = message.photo[-1].file_id
    elif message.text and message.text not in COMMANDS_LIST:
        new_data = message.text
    else:
        logging.info("get course info error")

    if new_data:
        course_exists = await db.course_exists(course_id=int(course_num))
        if course_exists:
            logging.info("update data")
            await db.update_course_data(triger=triger, value=new_data, id=int(course_num))
            await asyncio.sleep(3)
            await message.answer("Ma'lumot O'zgardi", reply_markup=await cource_data_info_btn(course_num=int(course_num)))
        else:
            if triger == "_title":
                logging.info("add title")
                await db.add_course(course_title=new_data)
            elif triger == "_discription":
                logging.info("add discription")
                await db.add_course(course_discription=new_data)
            elif triger == "_img_url":
                await db.add_course(course_img_url=new_data)
            elif triger == "_plan":
                logging.info("add plan")
                await db.add_course(course_plan=new_data)
            elif triger == "_price":
                logging.info("add price")
                await db.add_course(course_price=new_data)
            elif triger == "_discount":
                logging.info("add discount")
                await db.add_course(course_discount=new_data)
            await asyncio.sleep(3)
            await message.answer("Ma'lumot qo'shildi", reply_markup=await cource_data_info_btn(course_num=int(course_num)))
        # try:
        await state.finish()
        # except KeyError as e:
        #     logging.info(f"State ne zavershon 1: \n\n{e}")
        # finally:
        #     logging.info("Finally 3")
        
    else:
        if triger == "_title":
            msg = "Kurs sarlavhasini kiriting"
        elif triger == "_discription":
            msg = "Kurs haqidagi ma'lumotni kiriting"
        elif triger == "_img_url":
            msg = "Kurs rasmini kiriting"
        elif triger == "_plan":
            msg = "Kurs rejasini kiriting"
        elif triger == "_price":
            msg = "Kurs narxini so'm da kiriting"
        elif triger == "_discount":
            msg = "Kursga chegirma bo'lsa kiriting, aks holda 0 ni kiriting"
        await message.answer(msg)


@dp.message_handler(state=GetCourseTitle.title, content_types="text")
async def save_course_title(message: types.Message, state: FSMContext):
    logging.info('post course title')
    data = await state.get_data()
    call = data.get("call")
    logging.info(call)
    triger, course_num = str(call).split(":")
    logging.info(triger)
    await post_data_to_db(message=message, triger=triger, course_num=course_num, state=state)

@dp.message_handler(state=GetCourseDiscription.discription, content_types="text")
async def save_course_discription(message: types.Message, state: FSMContext):
    logging.info('post course discription')
    data = await state.get_data()
    call = data.get("call")
    logging.info(call)
    triger, course_num = str(call).split(":")
    logging.info(triger)
    await post_data_to_db(message=message, triger=triger, course_num=course_num, state=state)

@dp.message_handler(state=GetCourseImgUrl.img_url, content_types=types.ContentType.PHOTO)
async def save_course_image_url(message: types.Message, state: FSMContext):
    logging.info('post course image url')
    data = await state.get_data()
    call = data.get("call")
    logging.info(call)
    triger, course_num = str(call).split(":")
    logging.info(triger)
    await post_data_to_db(message=message, triger=triger, course_num=course_num, state=state)

@dp.message_handler(state=GetCoursePlan.plan, content_types="text")
async def save_course_plan(message: types.Message, state: FSMContext):
    logging.info('post course plan')
    data = await state.get_data()
    call = data.get("call")
    logging.info(call)
    triger, course_num = str(call).split(":")
    logging.info(triger)
    await post_data_to_db(message=message, triger=triger, course_num=course_num, state=state)

@dp.message_handler(state=GetCoursePrice.price, content_types="text")
async def save_course_price(message: types.Message, state: FSMContext):
    logging.info('post course price')
    data = await state.get_data()
    call = data.get("call")
    logging.info(call)
    triger, course_num = str(call).split(":")
    logging.info(triger)
    await post_data_to_db(message=message, triger=triger, course_num=course_num, state=state)

@dp.message_handler(state=GetCourseDiscount.discount, content_types="text")
async def save_course_discount(message: types.Message, state: FSMContext):
    logging.info('post course discount')
    data = await state.get_data()
    call = data.get("call")
    logging.info(call)
    triger, course_num = str(call).split(":")
    logging.info(triger)
    await post_data_to_db(message=message, triger=triger, course_num=course_num, state=state)

    # new_data = ""
    # if message.photo and triger=="_img_url":
    #     new_data = message.photo[-1].file_id
    # elif message.text and message.text not in COMMANDS_LIST:
    #     new_data = message.text
    # else:
    #     logging.info("get course info error")

    # if new_data:
    #     course_exists = await db.course_exists(course_id=int(course_num))
        # if course_exists:
        #     logging.info("update data")
        #     await db.update_course_data(triger=triger, value=new_data, id=int(course_num))
        #     await message.answer("Ma'lumot O'zgardi", reply_markup=await cource_data_info_btn(course_num=int(course_num)))
        # else:
        #     if triger == "_title":
        #         logging.info("add title")
        #         await db.add_course(course_title=new_data)
        #     elif triger == "_discription":
        #         logging.info("add discription")
        #         await db.add_course(course_discription=new_data)
        #     elif triger == "_img_url":
        #         await db.add_course(course_img_url=new_data)
        #     elif triger == "_plan":
        #         logging.info("add plan")
        #         await db.add_course(course_plan=new_data)
        #     elif triger == "_price":
        #         logging.info("add price")
        #         await db.add_course(course_price=new_data)
        #     elif triger == "_discount":
        #         logging.info("add discount")
        #         await db.add_course(course_discount=new_data)
        #     await message.answer("Ma'lumot qo'shildi", reply_markup=await cource_data_info_btn(course_num=int(course_num)))
        # try:
        #     await state.finish()
        # except Exception as e:
        #     logging.info(f"State ne zavershon 1: \n\n{e}")
        # finally:
        #     logging.info("Finally 3")

    # else:
    #     if triger == "_title":
    #         msg = "Kurs sarlavhasini kiriting"
    #     elif triger == "_discription":
    #         msg = "Kurs haqidagi ma'lumotni kiriting"
    #     elif triger == "_img_url":
    #         msg = "Kurs rasmini kiriting"
    #     elif triger == "_plan":
    #         msg = "Kurs rejasini kiriting"
    #     elif triger == "_price":
    #         msg = "Kurs narxini so'm da kiriting"
    #     elif triger == "_discount":
    #         msg = "Kursga chegirma bo'lsa kiriting, aks holda 0 ni kiriting"
    #     await message.answer(msg)



